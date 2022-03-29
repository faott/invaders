import pygame
from random import randint, choice
from rockets import Rockets
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

    def shoot(self, shots):

        enemy_shot = Rockets(self.x + self.size/2, self.y + self.size + 5, 15, 5)
        shots.append(enemy_shot)

        return shots


