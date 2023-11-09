import pygame
import sys
from telaScoreboard.scores import show_scoreboard
from telaInstrucao.instructions import instructions
import subprocess

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

sound_enabled = True

def start_game():
    subprocess.run(['python', 'jogo/game_platform/jogo.py'])

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def main_menu():
    global sound_volume
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    # Start Game
                    pygame.mixer.music.set_volume(0)
                    start_game()
                    pygame.mixer.music.set_volume(0.5)
                elif instructions_button_rect.collidepoint(event.pos):
                    # Show Instructions
                    instructions()
                    pygame.mixer.music.load('musicas/back_music.mp3')
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                elif score_button_rect.collidepoint(event.pos):
                    show_scoreboard()
                    pygame.mixer.music.load('musicas/back_music.mp3')
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                elif quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        # Draw buttons
        x_button = (WIDTH - BUTTON_WIDTH) / 2
        start_button_rect = pygame.draw.rect(screen, BLACK, (x_button, 300, BUTTON_WIDTH, BUTTON_HEIGHT))
        instructions_button_rect = pygame.draw.rect(screen, BLACK, (x_button, 400, BUTTON_WIDTH, BUTTON_HEIGHT))
        score_button_rect = pygame.draw.rect(screen, BLACK, (x_button, 500, BUTTON_WIDTH, BUTTON_HEIGHT))
        quit_button_rect = pygame.draw.rect(screen, BLACK, (x_button, 855, BUTTON_WIDTH, BUTTON_HEIGHT))
        mute_button_rect = pygame.draw.rect(screen, BLACK, (50, 855, BUTTON_WIDTH, BUTTON_HEIGHT))
        
        screen.blit(background_image, (0, 0))

        draw_text("Start Game", FONT, WHITE, x_button + BUTTON_WIDTH - 100, 325)
        draw_text("Instructions", FONT, WHITE, x_button + BUTTON_WIDTH - 100, 425)
        draw_text("Scoreboard", FONT, WHITE, x_button + BUTTON_WIDTH - 100, 525)
        draw_text("Exit game", FONT, WHITE, x_button + BUTTON_WIDTH - 100, 880)
        draw_text("Mute", FONT, WHITE, 50 + BUTTON_WIDTH - 100, 880)
        pygame.display.update()

if __name__ == "__main__":
    main_menu()
