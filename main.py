import math
import pygame
import random
from constansts import *
from player import Player
from enemy import Enemy
from rockets import Rockets


# --------------
# INITIALIZATION
# --------------


# Feel free to adjust the values to fit your needs

pygame.init()  # type: ignore

pygame.display.set_caption('INVADERS')

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

background = pygame.image.load("media/background.png").convert_alpha()
game_over_surf = pygame.image.load("media/game_over.png").convert_alpha()


# ---------
# GAME LOOP
# ---------

running = True

player1 = Player(50, 50)
# enemy1 = Enemy(50, 30, 5, 30)

shots = []
enemys = []

# Initial definition to limit shooting rate of player
loaded = True
score = 0


def player_shoot():
    global loaded
    if loaded:
        shots.append(Rockets(player1.x + player1.width/2, player1.y - 32, -15, 5, colour="WHITE"))
        loaded = False

 
def spawn_enemys():
    enemy_offset = 0
    for x in range(random.randint(5,5)):
        enemys.append(Enemy(0 + enemy_offset, 30, 5, 30))
        enemy_offset += 100


def collision(cx1, cx2, cy1, cy2, r1, r2):
    dx = cx2 - cx1
    dy = cy2 - cy1

    distance = math.sqrt(dx * dx + dy * dy)

    if distance <= r1 + r2:
        return True
    else:
        return False

# Initial spawn of enemy- set

spawn_enemys()

# Defining User-events

enemy_shooting = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_shooting, random.randint(900, 1500))

enemy_spawn = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_spawn, 5000)

# Reload the players gun

reload = pygame.USEREVENT + 3
pygame.time.set_timer(reload, 800)


while running:
    
    clock.tick(30)
    screen.blit(background, (0,0))

    shots_left = []
    enemys_left = []
 
    # Event handling

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # type: ignore
            running = False
            break

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # type: ignore
            player_shoot()

    # Enemy spawn   
  
        if event.type == enemy_spawn:
            spawn_enemys()

        if event.type == reload:
            loaded = True


    # Enemy shots

        if event.type == enemy_shooting and enemys:
            shooter = random.choice(enemys)
            enemy_shot = Rockets(shooter.x + shooter.size/2, shooter.y + shooter.size + 5, 15, 5)
            shots.append(enemy_shot)
    
    # Enemy shots alternative

    for e in enemys:
        if random.randint(1,50) == 2:
            enemy_shot = Rockets(e.x + e.size/2, e.y + e.size + 5, 15, 5)
            shots.append(enemy_shot)
 
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
    player1.draw(screen)

    # Checking the shots if they collide with the player

    for s in shots:
        if collision((player1.x + player1.width / 2), s.x, (player1.y + player1.height / 2), s.y, player1.width / 2, s.size):
            pygame.quit()
            exit()

    # Checking if the shots collide with enemys but only if the shots are go upwards (no enemy friendly fire)
        else:
            for e in enemys:
                if collision(e.x, s.x, e.y, s.y, e.size, s.size) and s.speed < 0:
                    s.destroyed = True
                    e.destroyed = True
                    score += 1
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

    

#    pygame.draw.circle(screen, enemy_colour, (int(enemy_pos_x + 200), enemy_pos_y), enemy_size)
#    pygame.draw.circle(screen, enemy_colour, (int(enemy_pos_x + 400), enemy_pos_y), enemy_size)

    pygame.display.update()
    
pygame.quit()
exit()