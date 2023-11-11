import pygame
import csv
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1920, 1080
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
FONT = pygame.font.Font('telaScoreboard/fonts/arcade.ttf', 42)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scoreboard")

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def show_scoreboard():
    pygame.mixer.music.load("telaScoreboard/musicas/boardmusic.mp3")
    # Play the background music
    pygame.mixer.music.play(-1)  # -1 to loop the music indefinitely

    # Adjust the volume (optional)
    pygame.mixer.music.set_volume(0.3)  # Adjust the volume level (0.0 to 1.0)
    
    scores = []
    try:
        with open('telaScoreboard/scores.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                player_name, score = row[0], int(row[1])
                scores.append((player_name, score))
        # Order the scores by the score value
        scores = sorted(scores, key=lambda x: x[1], reverse=True)
        
    except FileNotFoundError:
        print("Score file not found.")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    pygame.mixer.music.stop()
                    return  # Return to the main menu if "M" is pressed

        # Clear the screen
        screen.fill(BLACK)

        # Display the scoreboard
        draw_text("TOP  BEST  PLAYERS", FONT, WHITE, WIDTH // 2, 180)
        draw_text("RANK", FONT, GREEN, (WIDTH // 2) - 300, 300)
        draw_text("NOME", FONT, GREEN, (WIDTH // 2), 300)
        draw_text("SCORE", FONT, GREEN, (WIDTH // 2) + 300, 300)
        draw_text("Pressione  M  para  ir  ao  menu", FONT, GREEN, (WIDTH // 2), 1000)

        y_position = 350
        for i, (player_name, score) in enumerate(scores[:10], start=1):
            draw_text(f"{i}", FONT, WHITE, (WIDTH // 2) - 300, y_position)
            draw_text(f"{player_name}", FONT, WHITE, WIDTH // 2, y_position)
            draw_text(f"{score}", FONT, WHITE, (WIDTH // 2) + 300, y_position)
            y_position += 60

        pygame.display.update()