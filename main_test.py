import pygame
import random

# --------------
# INITIALIZATION
# --------------


# Feel free to adjust the values to fit your needs

WIDTH, HEIGHT = 800,600
pygame.init()  # type: ignore

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
last_enemy_pos_x = 700

enemy_count = 3
enemy_offset = (last_enemy_pos_x - enemy_pos_x ) // (enemy_count -1)

enemy_colour = RED

player_width = 100
player_height = 20
player_pos_x = WIDTH//2 - player_width//2
player_pos_y = HEIGHT - player_height

offset = 0


while running:
    
    # Limit the framerate to 30 frames per second
    clock.tick(30)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # type: ignore
            running = False
            break
   
    # Draw game:
    screen.fill(WHITE)

    for e in range(enemy_count):
        pygame.draw.circle(screen, enemy_colour, (int(enemy_pos_x + offset), enemy_pos_y), enemy_size)
        offset += enemy_offset
    
    enemy_pos_x += enemy_speed

    if enemy_pos_x + last_enemy_pos_x >= WIDTH - enemy_size or enemy_pos_x <= 0 + enemy_size:
        enemy_speed *= -1*1.1
        enemy_pos_y += random.randint(10,20)
        enemy_colour = random.choice(colours_list[1:])










    # Draw Player

    pygame.draw.rect(screen, BLUE, (player_pos_x, player_pos_y, player_width, player_height))

    # Finally: Update the display
    pygame.display.update()
    
#END GAME LOOP


pygame.quit()  # type: ignore
exit()