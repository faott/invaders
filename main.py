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

pygame.display.set_caption('PLAYGROUND')

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

background = pygame.image.load("media/background.png").convert_alpha()


# ---------
# GAME LOOP
# ---------

running = True

player1 = Player(70, 70)
enemy1 = Enemy(50, 30, 5, 20)

shots = []

while running:
    
    # Limit the framerate to 30 frames per second
    clock.tick(30)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # type: ignore
            running = False
            break
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            shot = Rockets(player1.x + player1.width/2, player1.y, -15, 10)
            shots.append(shot)
   
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

    # Draw game:
    screen.blit(background, (0,0))

    player1.update()
    player1.draw(screen)

    enemy1.update()
    enemy1.draw(screen)

    for s in shots:
        shot.update()

    shots_left = []
    for s in shots:
        if not shot.destroyed:
            shots_left.append(s)

    shots = shots_left

    for s in shots:
        shot.draw(screen)

#    pygame.draw.circle(screen, enemy_colour, (int(enemy_pos_x + 200), enemy_pos_y), enemy_size)
#    pygame.draw.circle(screen, enemy_colour, (int(enemy_pos_x + 400), enemy_pos_y), enemy_size)

    # Finally: Update the display
    pygame.display.update()
    
#END GAME LOOP


pygame.quit()  # type: ignore
exit()