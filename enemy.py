import pygame
from random import randint, choice
from rockets import Rockets
from constansts import *
from vector import Vector




class Enemy:
    def __init__(self, pos, speed, size, type):

        self.pos = pos # Should be a Vector
        #self.x = x
        #self.y = y
        self.move = Vector(0,0)
        self.speed = speed
        self.size = size
        self.type = type
        self.destroyed = False

    def update(self):

        self.pos.x += self.speed
        #self.x += self.speed

        if self.pos.x >= WIDTH - self.size or self.pos.x <= 0:
            self.speed *= -1*1.1
            self.pos.y += randint(30,50)

    def draw(self, screen):

        screen.blit(self.type, (self.pos.x, self.pos.y))

    def shoot(self, shots):

        enemy_shot = Rockets(self.pos.x + self.size/2, self.pos.y + self.size + 5, 15, 5)
        shots.append(enemy_shot)

        return shots


