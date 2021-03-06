import pygame
from constants import *
from rockets import Rockets
from vector import Vector


class Player(pygame.sprite.Sprite):
    
    def __init__(self, ship='default'):

        super().__init__()

        self.vel = Vector(0,0)
        self.speed = 8
        self.loaded = True
        self.reloadtime = 800
        self.lives = 3
        self.score = 0
        self.ship = ship
        self.last_ship = self.ship
        
        self.explosion_img = pygame.image.load(explosion_img['enemy']).convert_alpha()
        self.image = pygame.image.load(player_icon[ship]).convert_alpha()
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT - 100))
        self.shoot_sound = pygame.mixer.Sound("sound/player_shoot.wav")
        self.explosion_sound = pygame.mixer.Sound("sound/explosion.wav")
        self.shoot_sound.set_volume(0.25)
        self.explosion_sound.set_volume(0.25)

    def update(self):

        if self.ship != self.last_ship:
            actual_pos = (self.rect.centerx, self.rect.centery)     # type: ignore
            self.image = pygame.image.load(player_icon[self.ship]).convert_alpha()
            self.rect = self.image.get_rect(center=(actual_pos))

        self.rect.move_ip(self.vel.x, self.vel.y)  # type: ignore

        if self.rect.left < 0:          # type: ignore
            self.rect.right = WIDTH     # type: ignore

        if self.rect.right > WIDTH:     # type: ignore
            self.rect.left = 0          # type: ignore
                        
        if self.rect.top < 0:         # type: ignore
            self.rect.top = 0         # type: ignore

        if self.rect.bottom > 600:      # type: ignore
            self.rect.bottom = 600      # type: ignore
    



    def shoot(self, sprite_group):

        if self.loaded:
            
            self.shoot_sound.play()
            Rockets(self.rect.midtop, -15, WHITE, sprite_group)    # type: ignore
            self.loaded = False

    def hit(self, screen):

        self.explosion_sound.play()
        self.lives -= 1

        screen.blit(self.explosion_img, (self.rect.x - 30, self.rect.y - 30)) # type: ignore


