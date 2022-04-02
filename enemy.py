import pygame
from random import randint, choice
from rockets import Rockets
from constansts import *
from vector import Vector


class Enemy(pygame.sprite.Sprite):

    def __init__(self, pos, speed, size, type):

        super().__init__()

        self.pos = pos # Should be a Vector
        self.move = Vector(0,0)
        self.speed = speed
        self.type = type
        self.destroyed = False
        self.vel = Vector(0,0)

        self.enemy_img_1 = pygame.image.load("media/enemy1_30.png").convert_alpha()
        self.enemy_img_2 = pygame.image.load("media/enemy2_30.png").convert_alpha()
        self.enemy_img_3 = pygame.image.load("media/enemy3_30.png").convert_alpha()
        self.enemy_img_4 = pygame.image.load("media/enemy4_30.png").convert_alpha()

        self.enemy_img_list = [self.enemy_img_1, self.enemy_img_2, self.enemy_img_3, self.enemy_img_4]

        self.image = choice(self.enemy_img_list)
        self.rect = self.image.get_rect(topleft=(self.pos.x, self.pos.y))

        # Copy from playerclass ----> CHANGE
        self.explosion_img = pygame.image.load("media/explosion.png").convert_alpha()
        self.shoot_sound = pygame.mixer.Sound("sound/player_shoot.wav")
        self.explosion_sound = pygame.mixer.Sound("sound/explosion.wav")
        self.shoot_sound.set_volume(0.25)
        self.explosion_sound.set_volume(0.25)


    def update(self):

        self.rect.x += self.speed   # type: ignore

        if self.rect.right >= WIDTH or self.rect.left <= 0:    # type: ignore
            self.speed *= -1*1.1
            self.rect.y += randint(30,50)   # type: ignore

    def draw(self, screen):

        screen.blit(self.image, self.rect)

    def shoot(self, sprite_group):

        Rockets(self.rect.midbottom, 15, ORANGE, sprite_group)      # type: ignore

    def hit(self, screen):

        self.explosion_sound.play()
        screen.blit(self.explosion_img, (self.rect.x - 30, self.rect.y - 30)) # type: ignore


