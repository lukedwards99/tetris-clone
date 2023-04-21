import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('My Pygame Game with Multiple Surfaces')

# Set up the game clock
clock = pygame.time.Clock()
FPS = 60

# Create two surfaces with different colors
surface1 = pygame.Surface((200, 200))
surface1.fill((255, 0, 0))  # Red color

surface2 = pygame.Surface((200, 200))
surface2.fill((0, 255, 0))  # Green color

# Game loop
running = True
while running:
    # Set the frame rate
    elapsed_time = clock.tick(FPS)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game state
    # ...

    # Render game elements
    screen.fill((0, 0, 0))  # Clear the screen with black color

    # Blit the two surfaces onto the main screen
    screen.blit(surface1, (100, 100))
    screen.blit(surface2, (400, 300))

    # Update the display
    pygame.display.flip()

# Quit Pygame and close the window
pygame.quit()
sys.exit()
