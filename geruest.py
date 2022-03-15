import pygame


# --------------
# INITIALIZATION
# --------------

# Define height and width of the screen:
# Feel free to adjust the values to fit your needs
WIDTH, HEIGHT = 800,600

# Screen variable used to draw on
screen = pygame.display.set_mode((WIDTH,HEIGHT))

# Set title of game window
pygame.display.set_caption('PLAYGROUND')

pygame.init()  # type: ignore

# A few color definitions
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
GRAY = (100,100,100)
ORANGE = (242, 90, 15)

# clock is used to limit framerate for fast pcs
clock = pygame.time.Clock()

# ---------
# GAME LOOP
# ---------

running = True

while running:
    
    # Limit the framerate to 30 frames per second
    clock.tick(30)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # type: ignore
            running = False
            break
   
    # --------------------
    # TODO: Your code here


    # Draw background:
    screen.fill(WHITE)
            
    # Finally: Update the display
    pygame.display.update()
    
#END GAME LOOP


pygame.quit()  # type: ignore
exit()