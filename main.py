import pygame
import random

# --------------
# INITIALIZATION
# --------------


# Feel free to adjust the values to fit your needs

WIDTH, HEIGHT = 800,600
pygame.init()

pygame.display.set_caption('PLAYGROUND')

screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
GRAY = (100,100,100)
ORANGE = (242, 90, 15)

colours_list = [WHITE, BLACK, RED, GREEN, BLUE, GRAY, ORANGE]

# ---------
# GAME LOOP
# ---------

running = True

enemy_size = 30
enemy_speed = 15
enemy_pos_y = 0 + enemy_size
enemy_pos_x = 0 + enemy_size
enemy_colour = RED


while running:
    
    # Limit the framerate to 30 frames per second
    clock.tick(30)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
   
    # Draw game:
    screen.fill(WHITE)

    pygame.draw.circle(screen, enemy_colour, (enemy_pos_x, enemy_pos_y), enemy_size)
    enemy_pos_x += enemy_speed

    if enemy_pos_x >= WIDTH - enemy_size or enemy_pos_x <= 0 + enemy_size:
        enemy_speed *= -1 * 1.1
        enemy_pos_y += random.randint(5,15)
        enemy_colour = random.choice(colours_list[1:])

    # Finally: Update the display
    pygame.display.update()
    
#END GAME LOOP


pygame.quit()
exit()