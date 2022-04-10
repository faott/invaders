import pygame
from random import randint, choice
from rockets import Rockets
from constants import *
from vector import Vector


class Enemy(pygame.sprite.Sprite):

    def __init__(self, pos, speed):

        super().__init__()

        self.pos = pos # Should be a Vector
        self.move = Vector(0,0)
        self.speed = speed
        self.destroyed = False
        self.vel = Vector(0,0)

        # Media path stored in settings.py
        self.image = pygame.image.load(choice(enemy__icon_small)).convert_alpha()
        self.rect = self.image.get_rect(topleft=(self.pos.x, self.pos.y))

        # Copy from playerclass ----> CHANGE
        self.explosion_img = pygame.image.load(explosion_img['player1']).convert_alpha()
        self.shoot_sound = pygame.mixer.Sound("sound/player_shoot.wav")
        self.explosion_sound = pygame.mixer.Sound("sound/explosion.wav")
        self.shoot_sound.set_volume(0.25)
        self.explosion_sound.set_volume(0.25)


    def update(self):

        self.rect.x += self.speed   # type: ignore

        if self.rect.right >= WIDTH or self.rect.left <= 0:    # type: ignore
            self.speed *= -1*1.1
            self.rect.y += randint(30,50)   # type: ignore


    def shoot(self, sprite_group):

        Rockets(self.rect.midbottom, 15, ORANGE, sprite_group)      # type: ignore

    def hit(self, screen):

        self.explosion_sound.play()
        screen.blit(self.explosion_img, (self.rect.x - 30, self.rect.y - 30)) # type: ignore


class BossEnemy(pygame.sprite.Sprite):

    
    def __init__(self, pos, sprite_group):

        super().__init__(sprite_group)

        self.image = pygame.image.load(enemy__icon_boss[0]).convert_alpha()
        self.rect = self.image.get_rect(center=(pos))
        self.lives = 4
        self.pos = pos
        self.speed = 20
        self.timer = 0
        self.sprite_group = sprite_group

        self.explosion_sound = pygame.mixer.Sound(explosion_snd['default'])
        self.explosion_img = pygame.image.load(explosion_img['enemy']).convert_alpha()

    def update(self):

        self.timer += 0.1


        #if self.rect.top < 50:
            #self.rect.y += self.speed


        if self.timer > 1.5:

            # Random choose dirrection from tuple x or y
            direction = ['x','y']
            #direction = choice(direction)

            if choice(direction) == 'x':
                self.rect.x += self.speed
            else:
                self.rect.y += self.speed

            self.timer = 0

        if self.lives == 0:
            self.sprite_group.remove(self)

    # Reverse direction after hitting boundaries

        if self.rect.right >= WIDTH or self.rect.left <= 0 or self.rect.top <= 0 or self.rect.bottom >= HEIGHT:

            self.speed *= -1

    def hit(self, screen):

        self.explosion_sound.play()
        screen.blit(self.explosion_img, (self.rect.x - 30, self.rect.y - 30)) # type: ignore
        self.lives -= 1
