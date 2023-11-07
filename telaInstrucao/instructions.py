import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1920, 1080
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font('telaInstrucao/fonts/Blomberg.otf', 36)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Menu")
background_image = pygame.image.load('telaInstrucao/images/instructions_image.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
arrows_image_up = pygame.image.load('telaInstrucao/images/pixels_arrows-UP.png')
arrows_image_up = pygame.transform.scale(arrows_image_up, (300, 200))
arrows_image_LR = pygame.image.load('telaInstrucao/images/pixels_arrows-LR.png')
arrows_image_LR = pygame.transform.scale(arrows_image_LR, (300, 200))

image_directory_jump = "telaInstrucao/images/characterJump"
image_directory_walk = "telaInstrucao/images/characterWalk"

images_names_jump = ["character_malePerson_run0.png","character_malePerson_run1.png","character_malePerson_run2.png","character_malePerson_jump.png","character_malePerson_jump.png","character_malePerson_jump.png","character_malePerson_shove.png"]
images_jump = [pygame.image.load(os.path.join(image_directory_jump, img)) for img in images_names_jump]

images_names_walk = ["character_malePerson_walk0.png","character_malePerson_walk1.png","character_malePerson_walk2.png","character_malePerson_walk3.png","character_malePerson_walk4.png","character_malePerson_walk5.png","character_malePerson_walk6.png"]
images_walk = [pygame.image.load(os.path.join(image_directory_walk, img)) for img in images_names_walk]

# Initialize Pygame mixer
pygame.mixer.init()

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def instructions():
    current_image = 0
    pygame.mixer.music.load('telaInstrucao/musicas/back_music.mp3')
    pygame.mixer.music.set_volume(0.5)  # Set the volume to 50%
    pygame.mixer.music.play(-1)  # Play the background music on loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button_rect.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    return

        # Draw buttons
        x_button = (WIDTH - BUTTON_WIDTH) / 2
        quit_button_rect = pygame.draw.rect(screen, WHITE, (x_button, 855, BUTTON_WIDTH, BUTTON_HEIGHT))

        screen.blit(background_image, (0, 0))
        screen.blit(arrows_image_up, (400,400))
        screen.blit(arrows_image_LR, (1250,400))
        screen.blit(images_jump[current_image], (450, 130))
        screen.blit(images_walk[current_image], (1300, 130))
        current_image = (current_image + 1) % len(images_jump)
        draw_text("Main Menu", FONT, WHITE, x_button + BUTTON_WIDTH - 100, 880)
        # Display instructions
        draw_text("Instructions", FONT, WHITE, WIDTH // 2, 50)
        draw_text("Press the 'UP' Arrow Key to Jump", FONT, WHITE, 550, 650)
        draw_text("Press the Left or Right arrow key to move", FONT, WHITE, 1400, 650)

        draw_text("Avoid the Water and the Slimes", FONT, BLACK, WIDTH // 2, 750)

        pygame.time.delay(80)
        pygame.display.update()
                
