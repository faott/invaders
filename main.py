import math
import pygame
import random
from constansts import *
from player import Player
from enemy import Enemy
from rockets import Rockets
from vector import Vector


# --------------
# INITIALIZATION
# --------------

pygame.init()  # type: ignore

pygame.display.set_caption('INVADERS')

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

background_surf = pygame.image.load("media/background2.png").convert_alpha()


title_font = pygame.font.Font("font/AnachronautRegular-5VRB.ttf", 70)
default_font = pygame.font.Font("font/Uroob-Regular.ttf", 15)

titel_surf = title_font.render("INVADERS", True, WHITE)
instruction_surf = default_font.render("Press <Space> to Shoot, <Arrows> to Move!", True, WHITE)
replay_surf = default_font.render("Press <ENTER> to Start/Restart!", True, WHITE)
game_over_surf = title_font.render("Game Over", True, WHITE)


enemy_img_1 = pygame.image.load("media/enemy1_30.png").convert_alpha()
enemy_img_2 = pygame.image.load("media/enemy2_30.png").convert_alpha()
enemy_img_3 = pygame.image.load("media/enemy3_30.png").convert_alpha()
enemy_img_4 = pygame.image.load("media/enemy4_30.png").convert_alpha()

enemy_img_list = [enemy_img_1, enemy_img_2, enemy_img_3, enemy_img_4]

# ---------
# MENU
# ---------

mute_surf = pygame.image.load("media/mute.png").convert_alpha()
mute_rect = mute_surf.get_rect(midbottom = (WIDTH/2, HEIGHT-20))

# ---------
# SOUND
# ---------

# end_sound = pygame.mixer.Sound("sound/ending.wav")
# title_sound = pygame.mixer.Sound("sound/title_screen.wav")

def play_music(command):
   
    pygame.mixer.music.set_volume(0.3)

    playing_state = pygame.mixer.music.get_busy()
    print(playing_state)

    if command == "mute_unmute" and playing_state:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
    if command == "play":
        pygame.mixer.music.load("sound/level_1.wav")
        pygame.mixer.music.play(-1)
    if command == "mute_unmute" and not playing_state:
        pygame.mixer.music.load("sound/level_1.wav")
        pygame.mixer.music.play(-1)


# ---------
# TODO
# ---------

# Changing the Sound according to the Game States
# Creating different game states Menu, play, Game over


# ---------
# FUNCTIONS
# ---------

def start_game():

    player1.lives = 3
    player1.score = 0
    shots.clear()
    enemys.clear()
    spawn_enemys()

    return True

def spawn_enemys():
    enemy_offset = 0
    for x in range(random.randint(2,5)):
        enemys.append(Enemy(0 + enemy_offset, 30, 5, 30, random.choice(enemy_img_list)))
        enemy_offset += 100


def collision_shots(cx1, cx2, cy1, cy2, r1, r2):   
    dx = cx2 - cx1
    dy = cy2 - cy1

    distance = math.sqrt(dx * dx + dy * dy)

    if distance <= r1 + r2:
        return True
    else:
        return False

def collision_player(rect, shot):

    if type(rect) is Player:

        nx = max(rect.x , min(shot.x , rect.x + rect.width))
        ny = max(rect.y , min(shot.y , rect.y + rect.height))

        dx = nx - shot.x
        dy = ny - shot.y
        
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < shot.size:
            shots.remove(shot)
            player1.hit(screen)
    else:
        pass



# ---------
# USER EVENTS
# ---------


enemy_shooting = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_shooting, random.randint(700, 1100))

enemy_spawn = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_spawn, 5000)

# Reload the players gun

reload = pygame.USEREVENT + 3
pygame.time.set_timer(reload, 800)


player1 = Player(50, 50)
enemys = []
shots = []
running = False
music_mute = False

# ---------
# GAME MUSIC
# ---------

play_music("play")


# ---------
# GAME LOOP
# ---------

while True:

    clock.tick(30) 
    screen.blit(background_surf, (0,0))

    if not running:
        screen.blit(titel_surf, (60, 80))
        screen.blit(instruction_surf, (80, 200))
        screen.blit(replay_surf, (80,225))
        screen.blit(mute_surf, mute_rect)
        player1.draw(default_font, screen, 375, 275)
   
    shots_left = []
    enemys_left = []

    # Event handling

    for event in pygame.event.get():

        if event.type == pygame.QUIT:  # type: ignore
            pygame.quit()
            exit()
        
        if not running:
            mouse_pos = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed(3)

            if event.type == pygame.MOUSEBUTTONDOWN and mute_rect.collidepoint(mouse_pos):
                play_music(command="mute_unmute")

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # type: ignore
                running = start_game()
            
        if running:
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # type: ignore
                player1.shoot(shots)

            # Enemy spawn
            if event.type == enemy_spawn:
                spawn_enemys()

            if event.type == reload:
                player1.loaded = True

            # Choose a random enemy and shoot
            if event.type == enemy_shooting and enemys:
                random.choice(enemys).shoot(shots)
        
    if running:

        # Player movement reset to zero
        player1.vx = 0  
        player1.vy = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:  # type: ignore
            player1.vx = player1.speed
        elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:  # type: ignore
            player1.vx = -player1.speed
        elif keys[pygame.K_UP] and not keys[pygame.K_DOWN]:  # type: ignore
            player1.vy = -player1.speed
        elif keys[pygame.K_DOWN] and not keys[pygame.K_UP]:  # type: ignore
            player1.vy = player1.speed

        player1.update()
        player1.draw(default_font, screen, player1.x, player1.y)

        # Checking the shots if they collide with the player

        for s in shots:
            collision_player(player1, s)

            # Checking if the shots collide with enemys but only if the shots are go upwards (no enemy friendly fire)
            for e in enemys:
                if collision_shots(e.x, s.x, e.y, s.y, e.size, s.size) and s.speed < 0:
                    s.destroyed = True
                    e.destroyed = True
                    player1.score += 1
                else:
                    pass

        # Updating position and state of the shots
        for s in shots:
            s.update()
            if not s.destroyed:
                shots_left.append(s)

        shots = shots_left
        
        for s in shots:
            s.draw(screen)

        # Updating the position and state of the enemys
        for e in enemys:
            e.update()
            if not e.destroyed:
                enemys_left.append(e)

        enemys = enemys_left
    
        for e in enemys:
            e.draw(screen)

    # Stop game if game over
    if player1.lives == 0:
        running = False
        screen.blit(game_over_surf, (120,400))
        player1.draw(default_font, screen, 375, 275)

    pygame.display.update()