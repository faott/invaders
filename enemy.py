import pygame
from random import randint, choice
from constansts import *





class Enemy:
    def __init__(self, x, y, speed, size, type, colour=RED):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.colour = colour
        self.type = type
        self.destroyed = False

    def update(self):

        self.x += self.speed

        if self.x >= WIDTH - self.size or self.x <= 0:
            self.speed *= -1*1.1
            self.y += randint(30,50)
            self.colour = choice(colours_list[1:])

    def draw(self, screen):

        screen.blit(self.type, (self.x, self.y))
        # pygame.draw.circle(screen, self.colour, (int(self.x), self.y), self.size)





