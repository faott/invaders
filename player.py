import pygame
from constansts import *
from rockets import Rockets


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

        self.x += self.vx
        self.y += self.vy

        if self.x < 0:
            self.x = WIDTH - self.width
        elif self.x > WIDTH - self.width:
            self.x = 0

        self.y = max(self.y, self.height/2)
        self.y = min(self.y, HEIGHT - self.height)


    def draw(self, font, screen, x, y):

        screen.blit(self.player1_img, (x, y))
        score_surf = font.render(f"Score: {self.score}", True, WHITE)
        lives_surf = font.render(f"Lives: {self.lives}", True, WHITE)
        screen.blit(score_surf, (20, 580))
        screen.blit(lives_surf, (730, 580))

    
    def shoot(self, shots):


        if self.loaded:
            
            self.shoot_sound.play()
            shots.append(Rockets(self.x + self.width/2, self.y - 32, -15, 5, colour="WHITE"))
            self.loaded = False

        return shots

    def hit(self, screen):

        delay = 0
        self.explosion_sound.play()
        self.lives -= 1
        
        while delay <= 1:
           screen.blit(self.explosion_img, (self.x - 30, self.y - 30))
           delay += 0.01

