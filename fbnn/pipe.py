import pygame
import random
from defs import *

class Pipe():
    
    def __init__(self, gameDisplay, x, y, pipe_type):
        self.gameDisplay = gameDisplay
        self.state = pipe_moving
        self.pipe_type = pipe_type
        self.img = pygame.image.load(pipe_filename)
        self.rect = self.img.get_rect()
        if self.pipe_type == pipe_upper:
            y -= self.rect.height
        self.set_position(x, y)
        
    def set_position(self, x, y):
        self.rect.left = x
        self.rect.top = y
    
    def move_position(self, deltax, deltay):
        self.rect.centerx += deltax
        self.rect.centery += deltay
    
    def draw(self):
        self.gameDisplay.blit(self.img, self.rect)
    
    def check_status(self):
        if self.rect.right < 0:
            self.state = pipe_done
    
    def update(self, deltat):
        if self.state == pipe_moving:
            self.move_position(-(pipe_speed * deltat), 0)
            self.draw()
            self.check_status()

class PipeCollection():
    
    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.pipes = []
    
    def add_pair(self, x):
        top_y = random.randint(pipe_min, pipe_max - pipe_gap_size)
        bottom_y = top_y + pipe_gap_size
        
        p1 = Pipe(self.gameDisplay,x, top_y, pipe_upper)
        p2 = Pipe(self.gameDisplay,x, bottom_y, pipe_lower)
        
        self.pipes.append(p1)
        self.pipes.append(p2)
    
    def create_new_set(self):
        self.pipes = []
        placed = pipe_first
        
        while placed < display_w:
            self.add_pair(placed)
            placed += pipe_add_gap
            
    def update(self, deltat):
        rightmost = 0
        
        for p in self.pipes:
            p.update(deltat)
            
            if p.pipe_type == pipe_upper:
                if p.rect.left > rightmost:
                    rightmost = p.rect.left
                
        if rightmost < (display_w - pipe_add_gap):
            self.add_pair(display_w)
        
        self.pipes = [p for p in self.pipes if p.state == pipe_moving]