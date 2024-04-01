import pygame
import random
from defs import *

class Bird():
    
    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.state = bird_alive
        self.img = pygame.image.load(bird_filename)
        self.rect = self.img.get_rect()
        self.speed = 0
        self.time_lived = 0
        self.set_position(bird_start_x, bird_start_y)
        
    def set_position(self, x, y):
        self.rect.left = x
        self.rect.top = y
        
    def move(self, deltat):
        distance = 0
        new_speed = 0
        distance = (self.speed * deltat) + (0.5 * gravity * (deltat**2))
        new_speed = self.speed + (gravity * deltat)
        
        self.rect.centery += distance
        self.speed = new_speed
        
        if self.rect.top < 0:
            self.rect.top = 0
            self.speed = 0
    
    def jump(self):
        self.speed = bird_start_speed
    
    def draw(self):
        self.gameDisplay.blit(self.img, self.rect)
    
    def check_status(self, pipes):
        if self.rect.bottom > display_h:
            self.state = bird_dead
        else:
            self.check_hits(pipes)
    
    def check_hits(self, pipes):
        for p in pipes:
            if p.rect.colliderect(self.rect):
                self.state = bird_dead
                break
    
    def update(self, deltat, pipes):
        if self.state == bird_alive:
            self.time_lived += deltat
            self.move(deltat)
            self.draw()
            self.check_status(pipes)
            
class BirdCollection():
    
    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.birds = []
        self.create_new_generation()
    
    def create_new_generation(self):
        self.birds = []
        for i in range(0, generation_size):
            self.birds.append(Bird(self.gameDisplay))
    
    def update(self, deltat, pipes):
        num_alive = 0
        for b in self.birds:
            if random.randint(0,4) == 1:
                b.jump()
            b.update(deltat, pipes)
            if b.state == bird_alive:
                num_alive += 1
            
        return num_alive
                