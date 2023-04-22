import pygame as py
from assets import *
import sys

HEIGHT = 720
WIDTH = 720

UI_BORDER = 10

NUM_COLS = 10
NUM_ROWS = 20

GRID_BORDER_WIDTH = 2

board = list() #list to hold all the pieces on the playfield
board.append(Piece(NUM_ROWS, NUM_COLS, GRID_BORDER_WIDTH))


def main():
    py.init()
    screen = py.display.set_mode((HEIGHT, WIDTH))
    playSurface = py.Surface((WIDTH * .6 - UI_BORDER * 2, HEIGHT - UI_BORDER * 2))
    clock = py.time.Clock()
    py.display.set_caption('Tetris')
    running = True
    dt = 0
    font = py.font.Font(None, 36)

    player_pos = py.Vector2(screen.get_width() / 2, screen.get_height() / 2)

    while running:
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
                break
            # Check for KEYDOWN events
            if event.type == py.KEYDOWN:
                if event.key == py.K_UP:
                    pass #print("Up arrow key pressed")
                elif event.key == py.K_DOWN:
                    pass # print("Down arrow key pressed")
                elif event.key == py.K_LEFT:
                    board[len(board) - 1].moveleft()
                elif event.key == py.K_RIGHT:
                    board[len(board) - 1].moveright()
            
        DrawUI(playSurface)

        for piece in board:
            piece.draw(playSurface)

        screen.blit(playSurface, (UI_BORDER, UI_BORDER))

        fps_text = font.render(f"FPS: {clock.get_fps():.2f}", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))

        py.display.flip()

        dt = clock.tick(60) / 1000

    py.quit()
    sys.exit()
    

def DrawUI(surface: py.Surface) -> None:
    surface.fill((127,127,127))
    
    X_WIDTH = surface.get_width() / NUM_COLS
    Y_HEIGHT = surface.get_height() / NUM_ROWS


    # draw grid on surface that is NUM_COLS x NUM_ROWS
    for i in range(1,NUM_COLS):
        py.draw.line(surface, (120,120,120), (i * X_WIDTH, 0), (i * X_WIDTH, surface.get_height()), GRID_BORDER_WIDTH)
    for i in range(1,NUM_ROWS):
        py.draw.line(surface, (120,120,120), (0, i * Y_HEIGHT), (surface.get_width(), i * Y_HEIGHT), GRID_BORDER_WIDTH)

#print board to stdout
def printBoard():
    
    matrix = [["0" for j in range(NUM_COLS)] for i in range(NUM_ROWS)]

    for piece in board:
        for i in range(len(piece.matrix)):
            for j in range(len(piece.matrix[i])):
                if piece.matrix[i][j] == 1:
                    matrix[piece.x + i][piece.y + j] = "1"

    for row in matrix:
        print(row)

if __name__ == '__main__':
    # printBoard()
    main()