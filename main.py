import math
import pygame
import random
from constansts import *
from player import *
from enemy import Enemy
from rockets import Rockets
from vector import Vector

# --------------
# INITIALIZATION
# --------------

class Game:
    def __init__(self):

        self.state = {'start_menu': True, 'run':False, 'game_over': False, 'muted': False, 'paused':False}
        self.level = 1
        self.difficulty = 0
        self.enemys = []
        self.shots = []

        pygame.init()  # type: ignore

        pygame.display.set_caption('INVADERS')

        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock = pygame.time.Clock()

        self.background_surf = pygame.image.load("media/background2.png").convert_alpha()
        self.background_menu = pygame.image.load("media/background3.png").convert_alpha()

        self.title_font = pygame.font.Font("font/AnachronautRegular-5VRB.ttf", 70)
        self.default_font = pygame.font.Font("font/Uroob-Regular.ttf", 15)

        self.titel_surf = self.title_font.render("INVADERS", True, WHITE)
        self.instruction_surf = self.default_font.render("Press <Space> to Shoot, <Arrows> to Move!", True, WHITE)
        self.replay_surf = self.default_font.render("Press <ENTER> to Start/Restart!", True, WHITE)
        self.game_over_surf = self.title_font.render("Game Over", True, RED)
        self.paused_surf = self.title_font.render("Paused", True, WHITE)

        self.mute_surf = pygame.image.load("media/mute.png").convert_alpha()
        self.mute_rect = self.mute_surf.get_rect(midbottom = (WIDTH/2, HEIGHT-20))

    def draw_start_screen(self):

        self.screen.blit(self.background_menu, (0,0))
        self.screen.blit(self.titel_surf, (60, 80))
        self.screen.blit(self.instruction_surf, (80, 200))
        self.screen.blit(self.replay_surf, (80,225))
        self.screen.blit(self.mute_surf, self.mute_rect)

        self.screen.blit(player.image, (80, 280))           # type: ignore

    def draw_hud(self, score, lives):

        score_surf = self.default_font.render(f"Score: {score}", True, WHITE)
        lives_surf = self.default_font.render(f"Lives: {lives}", True, WHITE)   
        self.screen.blit(score_surf, (20, 580))
        self.screen.blit(lives_surf, (730, 580))     


    def draw_game_over(self):

        self.screen.blit(self.background_menu, (0,0))
        game.screen.blit(game.game_over_surf, (60, 80))
        self.screen.blit(self.instruction_surf, (80, 200))
        self.screen.blit(self.replay_surf, (80,225))
        #player.draw(game.default_font, game.screen)

    def play_music(self):
   
        pygame.mixer.music.set_volume(0.3)
        
        if self.state['start_menu']:
            pygame.mixer.music.load("sound/title_screen.wav")

        elif self.state['run'] and self.level == 1:
            pygame.mixer.music.load("sound/level_1.wav")

        else:
            pygame.mixer.music.load("sound/ending.wav")

        pygame.mixer.music.play(loops=-1, fade_ms=800)


    def pause(self): # change to display menu during game

        game.state['paused'] = not game.state['paused']
        #game.state['run'] = not game.state['run']


    def mute(self):

        playing = pygame.mixer.music.get_busy()
        self.state['muted'] = not self.state['muted']

        if playing:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def start_game(self):

        game.state['start_menu'] = False
        game.state['run'] = True
        player.lives = 3
        player.score = 0
        #game.shots.clear()
        #game.enemys.clear()
        #self.spawn_enemys()


    def spawn_enemys(self):
        enemy_offset = Vector(0,0)
        for x in range(random.randint(2,5)):
            #enemy_type = random.choice(self.enemy_img_list)
            enemy_type = 1
            enemy_pos = Vector(30,0)
            enemy_grp.add(Enemy(enemy_pos + enemy_offset, 5, 30, enemy_type))
            #self.enemys.append(Enemy(enemy_pos + enemy_offset, 5, 30, enemy_type))
            enemy_offset.x += 100

    def collision_player_enemy(self):

        collitions = pygame.sprite.groupcollide(player_grp, enemy_grp, False, True)

        if collitions:
            player.hit(self.screen)


    def collision_player_shots(self):

        collitions = pygame.sprite.groupcollide(enemy_grp, player_shot_grp, True, True)

        hits = collitions.keys()
        
        for enemy in hits:
            Enemy.hit(enemy, game.screen)  # type: ignore
            player.score += 1

        
    def collision_enemy_shots(self):

        collitions = pygame.sprite.groupcollide(player_grp, enemy_shot_grp, False, True)

        hits = collitions.keys()
        
        for enemy in hits:
            Player.hit(player, game.screen)  # type: ignore





game = Game()

player_grp = pygame.sprite.GroupSingle()
player = Player()
player_grp.add(player)

enemy_grp = pygame.sprite.Group()

enemy_shot_grp = pygame.sprite.Group()
player_shot_grp = pygame.sprite.Group()

game.play_music()

# ---------
# TODO
# ---------

# Changing the Sound according to the Game States
# Creating different game states Menu, play, Game over


# ---------
# FUNCTIONS
# ---------


# def collition_shot(object, shot):

#     if type(object) is Player:

#         nx = max(object.rect.x , min(shot.x , object.rect.x + object.width)) # type: ignore
#         ny = max(object.rect.y , min(shot.y , object.rect.y + object.height)) # type: ignore

#         dx = nx - shot.x
#         dy = ny - shot.y
        
#         distance = math.sqrt(dx * dx + dy * dy)

#         if distance < shot.size:
#             game.shots.remove(shot)
#             player.hit(game.screen)
#     else:
#         dx = (object.rect.x + object.size//2) - shot.x
#         dy = (object.rect.y + object.size//2) - shot.y

#         distance = math.sqrt(dx * dx + dy * dy)

#         if distance <= object.size + shot.size:
#             return True
#         else:
#             return False


# def collision_object():


#     if pygame.sprite.groupcollide(player_grp, enemy_grp, False, False):
#         print('collision')
        #player.lives = 0

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


# ---------
# GAME LOOP
# ---------

while True:

    game.clock.tick(30)

    # Draw the main menu

    if game.state['start_menu']:
        game.draw_start_screen()

    # Stop game if game over

    if player.lives == 0:
        game.state['run'] = False
        game.draw_game_over()

    # Draw the active game loop while playing

    if game.state['run'] and not game.state['paused']:

        player.vel = Vector(0,0)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:  # type: ignore
            player.vel.x = player.speed


        elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:  # type: ignore
            player.vel.x =- player.speed

        elif keys[pygame.K_UP] and not keys[pygame.K_DOWN]: 
            player.vel.y =- player.speed

        elif keys[pygame.K_DOWN] and not keys[pygame.K_UP]:  # type: ignore
            player.vel.y = player.speed

        game.screen.blit(game.background_surf, (0,0))  

        player_grp.update()
        player_grp.draw(game.screen)

        game.draw_hud(player.score, player.lives)

        enemy_grp.update()
        enemy_grp.draw(game.screen)

        player_shot_grp.update()
        player_shot_grp.draw(game.screen)

        enemy_shot_grp.update()
        enemy_shot_grp.draw(game.screen)

        game.collision_player_enemy()
        game.collision_player_shots()
        game.collision_enemy_shots()

    # ---------
    # EVENT HANDLING
    # ---------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:  # type: ignore
            pygame.quit()
            exit()
        
        if not game.state['run']:

            mouse_vel = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed(3)

            if event.type == pygame.MOUSEBUTTONDOWN and game.mute_rect.collidepoint(mouse_vel):
                game.mute()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # type: ignore
                game.start_game()
                game.play_music()
            
        if game.state['run']:
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # type: ignore
                player.shoot(player_shot_grp)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pass
                #game.pause()

            # Enemy spawn
            if event.type == enemy_spawn:
                game.spawn_enemys()

            if event.type == reload:
                player.loaded = True

            # Choose a random enemy and shoot
            if event.type == enemy_shooting and enemy_grp:
                enemy = random.choice(enemy_grp.sprites())
                enemy.shoot(enemy_shot_grp)                 # type: ignore
  
    pygame.display.update()