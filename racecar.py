import pygame
import time
import math
from utils import scale_image

GRASS = scale_image(pygame.image.load("img/grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("img/track.png"), 0.9)

TRACK_BORDER = scale_image(pygame.image.load("img/track-border.png"), 0.9)
FINISH = pygame.image.load("img/finish.png")

RED_CAR = pygame.image.load("img/car-red.png")

#WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing game!")

FPS = 60
clock = pygame.time.Clock()


run = True
while run:
    clock.tick(FPS)

    WIN.blit(GRASS,(0,0))
    WIN.blit(TRACK,(0,0))
    WIN.blit(FINISH,(0,0))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

pygame.quit()