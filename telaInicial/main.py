import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1920, 1080
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font('fonts/Blomberg.otf', 36)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Menu")
background_image = pygame.image.load('images/background_menu.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Initialize Pygame mixer
pygame.mixer.init()
pygame.mixer.music.load('musicas/back_music.mp3')
pygame.mixer.music.set_volume(0.5)  # Set the volume to 50%
pygame.mixer.music.play(-1)  # Play the background music on loop

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    # Start Game
                    print("Starting the game!")
                elif instructions_button_rect.collidepoint(event.pos):
                    # Show Instructions
                    print("Showing instructions!")
                elif options_button_rect.collidepoint(event.pos):
                    # Show Instructions
                    print("Showing options!")
                elif quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        # Draw buttons
        x_button = (WIDTH - BUTTON_WIDTH) / 2
        start_button_rect = pygame.draw.rect(screen, BLACK, (x_button, 300, BUTTON_WIDTH, BUTTON_HEIGHT))
        instructions_button_rect = pygame.draw.rect(screen, BLACK, (x_button, 400, BUTTON_WIDTH, BUTTON_HEIGHT))
        options_button_rect = pygame.draw.rect(screen, BLACK, (x_button, 500, BUTTON_WIDTH, BUTTON_HEIGHT))
        quit_button_rect = pygame.draw.rect(screen, BLACK, (x_button, 655, BUTTON_WIDTH, BUTTON_HEIGHT))

        screen.blit(background_image, (0, 0))

        draw_text("Start Game", FONT, WHITE, x_button + BUTTON_WIDTH - 100, 325)
        draw_text("Instructions", FONT, WHITE, x_button + BUTTON_WIDTH - 100, 425)
        draw_text("Options", FONT, WHITE, x_button + BUTTON_WIDTH - 100, 525)
        draw_text("Exit game", FONT, WHITE, x_button + BUTTON_WIDTH - 100, 680)
        
        pygame.display.update()

if __name__ == "__main__":
    main_menu()
