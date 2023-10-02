# Feito por:
# Bernardo Siqueira Esteves dos Reis - TIA
# Luis Henrique Bastos Tamura - TIA
# Vitor Sant'Ana Navarro - TIA 320.224-76

import pygame
from pygame.locals import *

pygame.init()

SCREEN_SIZE = (800, 600)
screen = pygame.display.set_mode(SCREEN_SIZE)

clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
