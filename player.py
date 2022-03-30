import pygame
from constansts import *
from rockets import Rockets
from vector import Vector


class Player:
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pos = Vector(WIDTH//2 - 25, HEIGHT - 50)
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - self.height
        self.move = Vector(0,0)
        self.speed = 8
        self.vx = 0
        self.vy = 0
        self.loaded = True
        self.reloadtime = 800
        self.lives = 3
        self.score = 0
        
        self.explosion_img = pygame.image.load("media/explosion.png").convert_alpha()
        self.player1_img = pygame.image.load("media/player1_50.png").convert_alpha()
        self.shoot_sound = pygame.mixer.Sound("sound/player_shoot.wav")
        self.explosion_sound = pygame.mixer.Sound("sound/explosion.wav")
        self.shoot_sound.set_volume(0.25)
        self.explosion_sound.set_volume(0.25)


    def update(self):

        self.pos += self.move
        #self.x += self.vx
        #self.y += self.vy

        if self.pos.x < 0:
            self.pos.x = WIDTH - self.width
        elif self.pos.x > WIDTH - self.width:
            self.pos.x = 0

        self.pos.y = max(self.pos.y, self.height/2)
        self.pos.y = min(self.pos.y, HEIGHT - self.height)


    def draw(self, font, screen):

        #screen.blit(self.player1_img, (x, y))
        screen.blit(self.player1_img, (self.pos.x, self.pos.y))
        score_surf = font.render(f"Score: {self.score}", True, WHITE)
        lives_surf = font.render(f"Lives: {self.lives}", True, WHITE)
        screen.blit(score_surf, (20, 580))
        screen.blit(lives_surf, (730, 580))

    
    def shoot(self, shots):


        if self.loaded:
            
            self.shoot_sound.play()
            shots.append(Rockets(self.pos.x + self.width/2, self.pos.y - 32, -15, 5, colour="WHITE"))
            self.loaded = False

        return shots

    def hit(self, screen):

        delay = 0
        self.explosion_sound.play()
        self.lives -= 1
        
        while delay <= 1:
           screen.blit(self.explosion_img, (self.pos.x - 30, self.pos.y - 30))
           delay += 0.01

