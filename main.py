import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1920, 1080
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font('telaGameOver/fonts/undertale.ttf', 60)
FONT2 = pygame.font.Font('telaGameOver/fonts/undertale.ttf', 32)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Game Over")

pygame.mixer.music.load("telaGameOver/musicas/gameOver_Sound.mp3")
# Play the background music
pygame.mixer.music.play(-1)  # -1 to loop the music indefinitely

# Adjust the volume (optional)
pygame.mixer.music.set_volume(0.5)  # Adjust the volume level (0.0 to 1.0)

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def game_over_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return
                    
        # Clear the screen
        screen.fill(WHITE)

        # Display "Game Over" message
        draw_text("GAME", FONT, BLACK, WIDTH // 2, (HEIGHT // 2) - 80)
        draw_text("OVER", FONT, BLACK, WIDTH // 2, HEIGHT // 2)
        draw_text("Você foi engolido pelas águas implacáveis.", FONT2, BLACK, WIDTH // 2, (HEIGHT // 2) + 150)
        draw_text("Pressione 'S' para voltar ao Menu Inicial", FONT2, BLACK, WIDTH // 2, (HEIGHT // 2) + 400)

        pygame.display.update()

if __name__ == "__main__":
    game_over_screen()
