import pygame
from pygame.locals import *
bg1 = pygame.image.load("shark.jpg")
bg2 = pygame.image.load("shark.jpg")
pos_x1 = 0
pos_x2 = 640
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Rolling BG Demo")
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        screen.blit(bg1, (pos_x1, 0))
        screen.blit(bg2, (pos_x2, 0))
        pos_x1 -= 0.5
        pos_x2 -= 0.5
        if pos_x1 < -640:
            pos_x1 = 640
        elif pos_x2 < -640:
            pos_x2 = 640
        pygame.display.update()