import pygame
import random
from constants import *
from player import *
from enemy import Enemy, BossEnemy
from rockets import Rockets
from vector import Vector
from debug import debug


class MenuItem(pygame.sprite.Sprite):

    def __init__(self, surface, pos, sprite_group, text=False):

        # Passes the sprite group to the super sprite class

        super().__init__(sprite_group)
        self.pos = pos
        self.sprite_group = sprite_group

        # Checks if item is text or image throu the default argument text
        # surface in the else statement has to be a suface (from get_text mthod in ex.)

        if not text:
            self.image = pygame.image.load(surface).convert_alpha()
        else:
            self.image = surface

        self.rect = self.image.get_rect(center=(self.pos))


class Game:
    def __init__(self, ship):

        self.state = {'start_menu': True, 'run':False, 'game_over': False, 'muted': False, 'paused':False}
        self.level = 1
        self.difficulty = 0
        #self.enemys = []
        #self.shots = []
        self.show_info = False
        self.ship = ship
       
        self.background_surf = pygame.image.load("media/background2.png").convert_alpha()
        self.background_menu = pygame.image.load("media/background3.png").convert_alpha()

        self.title_font = pygame.font.Font("font/AnachronautRegular-5VRB.ttf", 70)
        self.default_font = pygame.font.Font("font/Uroob-Regular.ttf", 25)

        self.replay_surf = self.default_font.render("Press <ENTER> to Start/Restart!", True, WHITE)
        self.game_over_surf = self.title_font.render("Game Over", True, WHITE)
        self.paused_surf = self.title_font.render("Paused", True, WHITE)

    def draw_hud(self, score, lives):

        score_surf = self.default_font.render(f"Score: {score}", True, WHITE)
        lives_surf = self.default_font.render(f"Lives: {lives}", True, WHITE)   
        screen.blit(score_surf, (20, 580))
        screen.blit(lives_surf, (730, 580))

    def play_music(self):
        
        pygame.mixer.music.set_volume(0.3)
        

        if self.state['start_menu']:
            pygame.mixer.music.load(background_snd['title'])

        elif self.state['run'] and self.level == 1:
            pygame.mixer.music.load(background_snd['level1'])

        elif self.state['game_over']:
            pygame.mixer.music.load(background_snd['ending'])

        pygame.mixer.music.play(loops=-1, fade_ms=800)



    def pause(self): # change to display menu during game

        self.state['paused'] = not self.state['paused']

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

        global enemy_count_small
        enemy_offset = Vector(0,0)

        for x in range(random.randint(2,5)):
            enemy_pos = Vector(30,0)
            enemy_grp.add(Enemy(enemy_pos + enemy_offset, 5))
            enemy_offset.x += 100
            enemy_count_small += 1

    def spawn_boss_enemy(self):

        if len(boss_enemy_grp) < 2:

            BossEnemy((200,110), boss_enemy_grp)

    def collision_player_enemy(self):

        collitions = pygame.sprite.groupcollide(player_grp, enemy_grp, False, True)

        if collitions:
            player.hit(screen)

    def collision_player_boss_enemy(self):

        collitions = pygame.sprite.groupcollide(boss_enemy_grp, player_grp, False, False)

        if collitions:
                player.lives = 0

    def collision_player_shots(self):

        collitions = pygame.sprite.groupcollide(enemy_grp, player_shot_grp, True, True)

        hits = collitions.keys()
        
        for enemy in hits:
            Enemy.hit(enemy, screen)  # type: ignore
            player.score += 1

    def collision_player_shot_boss(self):

        collitions = pygame.sprite.groupcollide(boss_enemy_grp, player_shot_grp, False, True)

        hits = collitions.keys()
        
        for enemy in hits:
            enemy.hit(screen)  # type: ignor
        
    def collision_enemy_shots(self):

        collitions = pygame.sprite.groupcollide(player_grp, enemy_shot_grp, False, True)

        hits = collitions.keys()
        
        for enemy in hits:
            Player.hit(enemy, screen)  # type: ignore


# ---------
# FUNCTIONS
# ---------


def get_text(text, size, colour=WHITE, type='uroob'):

    font = pygame.font.Font(font_types[type], size)
    surf = font.render(text, True, colour)

    return surf


def draw_start_screen():

    global animation_counter, ship_selection, menu_show_info    

    animation_counter += 0.1

    if animation_counter > 1.2:
        if ship_selection == 'player1_100':
            ship_ico_p1_100.image = pygame.transform.rotate(ship_ico_p1_100.image, 90)  # type: ignore

        if ship_selection == 'player2_100':
            ship_ico_p2_100.image = pygame.transform.rotate(ship_ico_p2_100.image, 90)  # type: ignore

        if ship_selection == 'player1_50':
            ship_ico_p1_50.image = pygame.transform.rotate(ship_ico_p1_50.image, 90)  # type: ignore

        if ship_selection == 'player2_50':
            ship_ico_p2_50.image = pygame.transform.rotate(ship_ico_p2_50.image, 90)  # type: ignore

        animation_counter = 0
    
    screen.blit(start_screen_surf, (0,0))
    start_menu_sprites.draw(screen)
    
    if menu_show_info:

        info_surf = pygame.surface.Surface((700,370))
        info_surf.fill(SPACE_BLUE)

        info_surf.blit(get_text("Press <Space> to Shoot, <Arrows> to Move!", 20), (80, 225))
        info_surf.blit(get_text("Press <ENTER> to Start/Restart!", 20), (80, 200))

        screen.blit(info_surf, (50,25))       
    
    # Returning the ship selection could be list later with two player and settings etc.

    return ship_selection

def draw_game_over():

    screen.blit(game.background_menu, (0,0))
    screen.blit(game.game_over_surf, (60, 80))
    game.play_music()

# ---------
# INIZIALISATION
# ---------

pygame.init()

pygame.display.set_caption('INVADERS')

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

# Inizialising the start screen variables / Path to media stored in constants.py

start_menu_sprites = pygame.sprite.Group()
start_screen_surf = pygame.image.load(background['start']).convert_alpha()
animation_counter = 0

info_btn = MenuItem(icons['information'], (320,430), start_menu_sprites)
mute_btn = MenuItem(icons['mute'], (400,430), start_menu_sprites)
set_btn = MenuItem(icons['settings'], (480,430), start_menu_sprites)

title = MenuItem(get_text("INVADERS", 70, WHITE, 'anarchonaut'), (400,80), start_menu_sprites, text=True)
select_ship = MenuItem(get_text("< < < SELECT your Ship ! > > >", 20), (400, 300), start_menu_sprites, text=True)

ship_ico_p1_50 = MenuItem(player_icon['player1_50'], (200,360), start_menu_sprites)
ship_ico_p1_100 = MenuItem(player_icon['player1_100'], (200,240), start_menu_sprites)
ship_ico_p2_50 = MenuItem(player_icon['player2_50'], (600,360), start_menu_sprites)
ship_ico_p2_100 = MenuItem(player_icon['player2_100'], (600,240), start_menu_sprites)

# Preset the ship selection to default value 
ship_selection = 'player1_100'
menu_show_info = False

game = Game(ship_selection)
 
player_grp = pygame.sprite.GroupSingle()
player = Player(ship_selection)
player_grp.add(player)

enemy_grp = pygame.sprite.Group()
boss_enemy_grp = pygame.sprite.Group()

enemy_shot_grp = pygame.sprite.Group()
player_shot_grp = pygame.sprite.Group()

# Counting the spawn of smalll enemys through the spawn_enemey function
enemy_count_small = 0

game.play_music()

# ---------
# OEN TASKS
# ---------

# Changing the Sound according to the Game States
# Creating different game states Menu, play, Game over
# counting score when killin boss enemy
# Look at module pickle (img und sound not pickleble)



# ---------
# USER EVENTS
# ---------


enemy_shooting = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_shooting, random.randint(700, 1100))

enemy_spawn = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_spawn, 5000)

boss_enemy_spawn = pygame.USEREVENT + 4
pygame.time.set_timer(boss_enemy_spawn, 10000)

# Reload the players gun

reload = pygame.USEREVENT + 3
pygame.time.set_timer(reload, 800)


# ---------
# GAME LOOP
# ---------

while True:

    game_time = clock.tick(30)
    
    # Draw the main menu

    if game.state['start_menu']:

        # Setting the player ship according to menu, set last ship at end of loop
        player.ship = draw_start_screen()

    # Stop game if game over

    if player.lives == 0:
        game.state['run'] = False
        game.state['game_over'] = True
        draw_game_over()
        game.play_music()

    # Draw the active game loop while playing

    if game.state['run'] and not game.state['paused']:

        player.vel = Vector(0,0)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            player.vel.x = player.speed

        elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            player.vel.x =- player.speed

        elif keys[pygame.K_UP] and not keys[pygame.K_DOWN]: 
            player.vel.y =- player.speed

        elif keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
            player.vel.y = player.speed

        screen.blit(game.background_surf, (0,0))  

        player_grp.update()
        player_grp.draw(screen)

        game.draw_hud(player.score, player.lives)

        enemy_grp.update()
        enemy_grp.draw(screen)

        boss_enemy_grp.update()
        boss_enemy_grp.draw(screen)

        player_shot_grp.update()
        player_shot_grp.draw(screen)

        enemy_shot_grp.update()
        enemy_shot_grp.draw(screen)

        game.collision_player_enemy()
        game.collision_player_boss_enemy()
        game.collision_player_shots()
        game.collision_enemy_shots()
        game.collision_player_shot_boss()

        player.last_ship = player.ship

    # ---------
    # EVENT HANDLING
    # ---------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if not game.state['run']:

            mouse_vel = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed(3)

            if event.type == pygame.MOUSEBUTTONDOWN and mute_btn.rect.collidepoint(mouse_vel): # type: ignore
                game.mute()

            if event.type == pygame.MOUSEBUTTONDOWN and info_btn.rect.collidepoint(mouse_vel): # type: ignore
                menu_show_info = not menu_show_info

            if event.type == pygame.MOUSEBUTTONDOWN and ship_ico_p1_100.rect.collidepoint(mouse_vel): # type: ignore
                ship_selection = 'player1_100'

            if event.type == pygame.MOUSEBUTTONDOWN and ship_ico_p2_100.rect.collidepoint(mouse_vel):  # type: ignore
                ship_selection = 'player2_100'

            if event.type == pygame.MOUSEBUTTONDOWN and ship_ico_p1_50.rect.collidepoint(mouse_vel):  # type: ignore
                ship_selection = 'player1_50'

            if event.type == pygame.MOUSEBUTTONDOWN and ship_ico_p2_50.rect.collidepoint(mouse_vel):  # type: ignore
                ship_selection = 'player2_50'

            if event.type == pygame.KEYDOWN and event.key == pygame.K_i:  # type: ignore
                menu_show_info = not menu_show_info

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

            if event.type == boss_enemy_spawn:
                game.spawn_boss_enemy()

            if event.type == reload:
                player.loaded = True

            # Choose a random enemy and shoot
            if event.type == enemy_shooting and enemy_grp:
                enemy = random.choice(enemy_grp.sprites())
                enemy.shoot(enemy_shot_grp)

  
    pygame.display.update()