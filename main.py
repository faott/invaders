import math
import pygame
import random
from enum import Enum
from constansts import *
from player import Player
from enemy import Enemy
from rockets import Rockets
from vector import Vector


# --------------
# INITIALIZATION
# --------------

class Game:
    def __init__(self, players, enemys ):
        self.state = {'start_menu': True, 'level1': False, 'game_over': False, 'muted': False, 'paused':False}
        self.difficulty = 0
        pass


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

class GameState(Enum):
    MUTED = 0
    START = 1
    END = 2
    LEVEL = 3















def play_music(state):
   
    pygame.mixer.music.set_volume(0.3)
    playing_state = pygame.mixer.music.get_busy()
    print(playing_state)

    if state == GameState.MUTED and playing_state:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    if state == GameState.START:
        pygame.mixer.music.load("sound/level_1.wav")
        pygame.mixer.music.play(-1)

    if state == GameState.MUTED and not playing_state:
        pygame.mixer.music.load("sound/level_1.wav")
        pygame.mixer.music.play(-1)
        


# ---------
# TODO
# ---------

# Changing the Sound according to the Game States
# Creating different game states Menu, play, Game over
# collision object überarbeiten
# change enemy do rect


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
    enemy_offset = Vector(0,0)
    for x in range(random.randint(2,5)):
        enemy_type = random.choice(enemy_img_list)
        enemy_pos = Vector(30,0)
        enemys.append(Enemy(enemy_pos + enemy_offset, 5, 30, enemy_type))
        enemy_offset.x += 100

def pause_game(paused):
        while not paused:
            pygame.time.wait(1000)
            return True


def collition_shot(object, shot):

    if type(object) is Player:

        nx = max(object.pos.x , min(shot.x , object.pos.x + object.width))
        ny = max(object.pos.y , min(shot.y , object.pos.y + object.height))

        dx = nx - shot.x
        dy = ny - shot.y
        
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < shot.size:
            shots.remove(shot)
            player1.hit(screen)
    else:
        dx = (object.pos.x + object.size//2) - shot.x
        dy = (object.pos.y + object.size//2) - shot.y

        distance = math.sqrt(dx * dx + dy * dy)

        if distance <= object.size + shot.size:
            return True
        else:
            return False




def collision_object(enemy, player):
    enemy_rect = enemy.type.get_rect(topleft = (200, 50))
    player_rect = player.player1_img.get_rect(topleft = (400, 550))
    if enemy_rect.colliderect(player_rect):
        player1.lives = 0


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
paused = False


# ---------
# GAME MUSIC
# ---------

play_music(GameState.START)


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
        player1.draw(default_font, screen)
   
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
                play_music(GameState.MUTED)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # type: ignore
                running = start_game()
            
        if running:
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # type: ignore
                player1.shoot(shots)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = not paused

            # Enemy spawn
            if event.type == enemy_spawn:
                spawn_enemys()

            if event.type == reload:
                player1.loaded = True

            # Choose a random enemy and shoot
            if event.type == enemy_shooting and enemys:
                random.choice(enemys).shoot(shots)
        
    if running and not paused:

        player1.move = Vector(0, 0)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:  # type: ignore
            #player1.vx = player1.speed
            player1.move.x = player1.speed
        elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:  # type: ignore
            #player1.vx = -player1.speed
            player1.move.x =- player1.speed
        elif keys[pygame.K_UP] and not keys[pygame.K_DOWN]:  # type: ignore
            #player1.vy = -player1.speed
            player1.move.y =- player1.speed
        elif keys[pygame.K_DOWN] and not keys[pygame.K_UP]:  # type: ignore
            #player1.vy = player1.speed
            player1.move.y = player1.speed

        player1.update()
        player1.draw(default_font, screen)

        # Checking the shots if they collide with the player

        for s in shots:
            collition_shot(player1, s)

            # Checking if the shots collide with enemys but only if the shots are go upwards (no enemy friendly fire)
            for e in enemys:
                if collition_shot(e, s) and s.speed < 0:
                    s.destroyed = True
                    e.destroyed = True
                    player1.score += 1
                else:
                    pass
        
        for e in enemys:
            collision_object(e, player1)


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
        player1.draw(default_font, screen)

    pygame.display.update()