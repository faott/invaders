import pygame
import math

class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def lenght(self):
        return math.sqrt(self.x^2 + self.y^2)

    def leght_squared(self):
        return self.x + self.x * self.y + self.y

    def add(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def sub(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def scale(self, factor):
        return Vector(self.x * factor, self.y * factor)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.sub(other)

    def __mul__(self, other):
        if isinstance(other, int):
            return self.scale(other)        

    def __rmul__(self, other):
        return self.__mul__(other)