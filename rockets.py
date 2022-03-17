import pygame
from constansts import *


class Rockets:
    def __init__(self, x, y, speed, size, colour=ORANGE):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.colour = colour
        self.destroyed = False

    def update(self):
        self.y += self.speed
        if self.y < 0 or self.y > HEIGHT:
            self.destroyed = True

    def draw(self, screen):

        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.size)