import pygame
from defs import *
from pipe import PipeCollection
from bird import BirdCollection

def update_label(data, title, font, x, y, gameDisplay):
    label = font.render(f'{title} {data}', 1, data_font_color)
    gameDisplay.blit(label, (x,y))
    return y

def update_data_labels(gameDisplay, deltat, game_time, num_iterations, num_alive, font):
    y_pos = 10
    gap = 20
    x_pos = 10
    y_pos = update_label(round(1000/deltat,2),'FPS',font, x_pos, y_pos + gap, gameDisplay)
    y_pos = update_label(round(game_time/1000,2),'Game Time',font, x_pos, y_pos + gap, gameDisplay)
    y_pos = update_label(num_iterations,'Iteration',font, x_pos, y_pos + gap, gameDisplay)
    y_pos = update_label(num_alive,'Alive',font, x_pos, y_pos + gap, gameDisplay)
    


def run_game():
    
    pygame.init()
    gameDisplay = pygame.display.set_mode((display_w,display_h))
    pygame.display.set_caption('Learn To Fly')
    
    running = True
    bgImg = pygame.image.load(bg_filename)
    label_font = pygame.font.SysFont('monospace', data_font_size)
    pipes = PipeCollection(gameDisplay)
    pipes.create_new_set()
    birds = BirdCollection(gameDisplay)
    
    clock = pygame.time.Clock()
    deltat = 0
    game_time = 0
    num_iterations = 0
    
    while running:
        
        deltat = clock.tick(fps)
        game_time += deltat
        
        gameDisplay.blit(bgImg,(0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                running = False
        
        
        pipes.update(deltat)
        num_alive = birds.update(deltat, pipes.pipes)
        
        if num_alive == 0:
            pipes.create_new_set()
            game_time = 0
            birds.create_new_generation()
            num_iterations += 1
        
        update_data_labels(gameDisplay,deltat, game_time, num_iterations, num_alive, label_font)
        pygame.display.update()

if __name__ == '__main__':
    run_game()