from re import A
import pygame
import math

class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def lenght(self):
        return math.sqrt(self.x^2 + self.y^2)

    def leght_squared(self):
        pass

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
        pass
        

    def __rmul__(self, other):
        return Vector
    




a = Vector(1,1)
b = Vector(2,2)

print(a == b)

print(a.x,a.y)
print(b.x,b.y)

# print(c.x,c.y)