# Feito por:
# Bernardo Siqueira Esteves dos Reis - TIA
# Luis Henrique Bastos Tamura - TIA
# Vitor Sant'Ana Navarro - TIA 320.224-76

import pygame
from character import Character
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()

SCREEN_SIZE = (800, 600)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Água Serena")

# todo: add if to change character name
if True:
    character_name = "bob"
else:
    character_name = "lisa"

character_sprites = pygame.sprite.Group()

character = Character(character_name, 10, 10)
character_sprites.add(character)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_RIGHT, pygame.K_d]:
                # todo: add moving logic
                character.animate()

    screen.fill((255, 255, 255))
    character_sprites.draw(screen)
    character_sprites.update(0.2)
    pygame.display.flip()
    clock.tick(60)
