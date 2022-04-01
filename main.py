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

class Game:
    def __init__(self):

        self.state = {'start_menu': True, 'run':False, 'game_over': False, 'muted': False, 'paused':False}
        self.level = 1
        self.difficulty = 0
        self.enemys = []
        self.shots = []

        #self.players = players

        pygame.init()  # type: ignore

        pygame.display.set_caption('INVADERS')

        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock = pygame.time.Clock()

        self.background_surf = pygame.image.load("media/background2.png").convert_alpha()

        self.title_font = pygame.font.Font("font/AnachronautRegular-5VRB.ttf", 70)
        self.default_font = pygame.font.Font("font/Uroob-Regular.ttf", 15)

        self.titel_surf = self.title_font.render("INVADERS", True, WHITE)
        self.instruction_surf = self.default_font.render("Press <Space> to Shoot, <Arrows> to Move!", True, WHITE)
        self.replay_surf = self.default_font.render("Press <ENTER> to Start/Restart!", True, WHITE)
        self.game_over_surf = self.title_font.render("Game Over", True, RED)
        self.paused_surf = self.title_font.render("Paused", True, WHITE)

        self.mute_surf = pygame.image.load("media/mute.png").convert_alpha()
        self.mute_rect = self.mute_surf.get_rect(midbottom = (WIDTH/2, HEIGHT-20))

        self.enemy_img_1 = pygame.image.load("media/enemy1_30.png").convert_alpha()
        self.enemy_img_2 = pygame.image.load("media/enemy2_30.png").convert_alpha()
        self.enemy_img_3 = pygame.image.load("media/enemy3_30.png").convert_alpha()
        self.enemy_img_4 = pygame.image.load("media/enemy4_30.png").convert_alpha()

        self.enemy_img_list = [self.enemy_img_1, self.enemy_img_2, self.enemy_img_3, self.enemy_img_4]


    def draw_start_screen(self):

        self.screen.blit(self.titel_surf, (60, 80))
        self.screen.blit(self.instruction_surf, (80, 200))
        self.screen.blit(self.replay_surf, (80,225))
        self.screen.blit(self.mute_surf, self.mute_rect)
        player1.draw(self.default_font, self.screen)

    def draw_hud(self):
        pass

    def draw_game_over(self):
        game.state['run'] = False
        game.screen.blit(game.game_over_surf, (60, 80))
        self.screen.blit(self.instruction_surf, (80, 200))
        self.screen.blit(self.replay_surf, (80,225))
        player1.draw(game.default_font, game.screen)

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
        player1.lives = 3
        player1.score = 0
        game.shots.clear()
        game.enemys.clear()
        self.spawn_enemys()


    def spawn_enemys(self):
        enemy_offset = Vector(0,0)
        for x in range(random.randint(2,5)):
            enemy_type = random.choice(self.enemy_img_list)
            enemy_pos = Vector(30,0)
            self.enemys.append(Enemy(enemy_pos + enemy_offset, 5, 30, enemy_type))
            enemy_offset.x += 100



game = Game()

player1 = Player(50, 50)

game.play_music()

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


def collition_shot(object, shot):

    if type(object) is Player:

        nx = max(object.pos.x , min(shot.x , object.pos.x + object.width))
        ny = max(object.pos.y , min(shot.y , object.pos.y + object.height))

        dx = nx - shot.x
        dy = ny - shot.y
        
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < shot.size:
            game.shots.remove(shot)
            player1.hit(game.screen)
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


# ---------
# GAME LOOP
# ---------

while True:

    game.clock.tick(30)
    game.screen.blit(game.background_surf, (0,0))

    if game.state['start_menu']:
        game.draw_start_screen()
   
    shots_left = []
    enemys_left = []

    # Event handling

    for event in pygame.event.get():

        if event.type == pygame.QUIT:  # type: ignore
            pygame.quit()
            exit()


        
        if not game.state['run']:

            mouse_pos = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed(3)

            if event.type == pygame.MOUSEBUTTONDOWN and game.mute_rect.collidepoint(mouse_pos):
                game.mute()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:  # type: ignore
                game.start_game()
                game.play_music()
            
        if game.state['run']:
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # type: ignore
                player1.shoot(game.shots)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pass
                #game.pause()

            # Enemy spawn
            if event.type == enemy_spawn:
                game.spawn_enemys()

            if event.type == reload:
                player1.loaded = True

            # Choose a random enemy and shoot
            if event.type == enemy_shooting and game.enemys:
                random.choice(game.enemys).shoot(game.shots)
        
    
    if game.state['run'] and not game.state['paused']:

        player1.move = Vector(0, 0)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:  # type: ignore
            player1.move.x = player1.speed

        elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:  # type: ignore
            player1.move.x =- player1.speed

        elif keys[pygame.K_UP] and not keys[pygame.K_DOWN]:  # type: ignore
            player1.move.y =- player1.speed

        elif keys[pygame.K_DOWN] and not keys[pygame.K_UP]:  # type: ignore
            player1.move.y = player1.speed

        player1.update()
        player1.draw(game.default_font, game.screen)

        # Checking the shots if they collide with the player

        for s in game.shots:
            collition_shot(player1, s)

            # Checking if the shots collide with enemys but only if the shots are go upwards (no enemy friendly fire)
            for e in game.enemys:
                if collition_shot(e, s) and s.speed < 0:
                    s.destroyed = True
                    e.destroyed = True
                    player1.score += 1
                else:
                    pass
        
        for e in game.enemys:
            collision_object(e, player1)


        # Updating position and state of the shots
        for s in game.shots:
            s.update()
            if not s.destroyed:
                shots_left.append(s)

        game.shots = shots_left

        for s in game.shots:
            s.draw(game.screen)

        # Updating the position and state of the enemys
        for e in game.enemys:
            e.update()
            if not e.destroyed:
                enemys_left.append(e)

        game.enemys = enemys_left
    
        for e in game.enemys:
            e.draw(game.screen)

    # Stop game if game over
    if player1.lives == 0:
        game.draw_game_over()

    


    pygame.display.update()