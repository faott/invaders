import pygame
from constansts import *


class Player:
    
    def __init__(self, width, height, colour=RED):
        self.width = width
        self.height = height
        self.colour = colour
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - self.height
        self.speed = 8
        self.vx = 0
        self.vy = 0
    
    def update(self):

        self.x += self.vx
        self.y += self.vy

        if self.x < 0:
            self.x = WIDTH - self.width
        elif self.x > WIDTH - self.width:
            self.x = 0

        self.y = max(self.y, self.height/2)
        self.y = min(self.y, HEIGHT - self.height)


    def draw(self, screen):

        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
