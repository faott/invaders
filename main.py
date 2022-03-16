from curses import KEY_LEFT, KEY_RIGHT
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
enemy_colour = RED

player_width = 100
player_height = 20
player_pos_x = WIDTH//2 - player_width//2
player_pos_y = HEIGHT - player_height
player_speed = 8



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


    enemy1 = pygame.draw.circle(screen, enemy_colour, (int(enemy_pos_x), enemy_pos_y), enemy_size)
    enemy2 = pygame.draw.circle(screen, enemy_colour, (int(enemy_pos_x + 200), enemy_pos_y), enemy_size)
    enemy3 = pygame.draw.circle(screen, enemy_colour, (int(enemy_pos_x + 400), enemy_pos_y), enemy_size)
    enemy_pos_x += enemy_speed

    if enemy_pos_x + 400 >= WIDTH - enemy_size or enemy_pos_x <= 0 + enemy_size:
        enemy_speed *= -1*1.1
        enemy_pos_y += random.randint(10,20)
        enemy_colour = random.choice(colours_list[1:])
    
    # Draw Player
    pygame.draw.rect(screen, BLUE, (player_pos_x, player_pos_y, player_width, player_height))
    keys = pygame.key.get_pressed()
    move_x = 0
    move_y = 0
    
    if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:  # type: ignore
        move_x = player_speed
    if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:  # type: ignore
        move_x -= player_speed
    if keys[pygame.K_UP] and not keys[pygame.K_DOWN] and player_pos_y > 0:  # type: ignore
        move_y -= player_speed
    if keys[pygame.K_DOWN] and not keys[pygame.K_UP] and player_pos_y + player_height < HEIGHT:  # type: ignore
        move_y = player_speed

    player_pos_x += move_x
    player_pos_y += move_y

    if player_pos_x < 0:
        player_pos_x = WIDTH - player_width
    elif player_pos_x > WIDTH - player_width:
        player_pos_x = 0

    

    # Finally: Update the display
    pygame.display.update()
    
#END GAME LOOP


pygame.quit()  # type: ignore
exit()