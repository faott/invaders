import pygame
from constants import *
from vector import Vector


class Rockets(pygame.sprite.Sprite):

    def __init__(self, pos, speed, colour, sprite_group):

        # Passing the Argument Sprite Group to parent class (--> main.py)
        
        super().__init__(sprite_group)

        self.pos = pos
        self.colour = colour

        self.vel = Vector(0,speed)

        self.image = pygame.Surface((5,5))
        self.image.fill(colour)
        self.rect = self.image.get_rect(center=(self.pos[0], self.pos[1]))

        self.sprite_group = sprite_group

        #pygame.sprite.Group.add(self.sprite_group, self)
    


    def update(self):

        self.rect.move_ip(self.vel.x, self.vel.y)                   # type: ignore

        if self.rect.bottom < 0 or self.rect.top > HEIGHT:          # type: ignore
            pygame.sprite.Group.remove(self.sprite_group, self)


