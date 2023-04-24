import pygame as py
from enum import Enum
import random

class PieceType(Enum):
    I = 1
    L = 2
    T = 3

class Rotation(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

class GameObject:
    def __init__(self) -> None:
        pass

    def draw(self, surface: py.Surface) -> None:
        raise NotImplementedError("can not call draw on base class")

class Piece(GameObject):
    def __init__(self, num_rows: int, num_cols: int, grid_border_width: int) -> None:
        self.type = PieceType(random.randint(1, 3))
        self.rotation = Rotation(random.randint(1, 4))
        self.x = random.randint(0, num_cols - 1)
        self.y = 0
        self.matrix = []
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.placed = False

        self.NUM_ROWS = num_rows
        self.NUM_COLS = num_cols
        self.GRID_BORDER_WIDTH = grid_border_width

        if self.type == PieceType.I:
            self.matrix = [
                    [0, 1, 0],
                    [0, 1, 0],
                    [0, 1, 0]
                ]
        elif self.type == PieceType.L:
            self.matrix = [
                    [0, 1, 0],
                    [0, 1, 0],
                    [0, 1, 1]
                ]
        elif self.type == PieceType.T:
            self.matrix = [
                    [0, 1, 0],
                    [1, 1, 1],
                    [0, 0, 0]
                ]

    def rotate_90(self):
        return [list(reversed(row)) for row in zip(*self.matrix)]
    
    def rotate_90_counterclockwise(self):
        return [list(row) for row in zip(*reversed(self.matrix))]

    def movedown(self) -> bool:
        if self.y + len(self.matrix) < self.NUM_ROWS:
            self.y += 1
            return False
        else:
            self.placed = True
            return True
        
    
    def moveleft(self) -> None:
        self.x -= 1
    
    def moveright(self) -> None:
        self.x += 1

    # def drawL(self, surface: py.Surface) -> None:
    #     pass

    # def drawI(self, surface: py.Surface) -> None:
    #     pass

    # def drawT(self, surface: py.Surface) -> None:
    #     pass
    
    def draw(self, surface: py.Surface) -> None:
        
        X_WIDTH = surface.get_width() / self.NUM_COLS
        Y_HEIGHT = surface.get_height() / self.NUM_ROWS

        #draw a rect at self.x and self.y that is X_WIDTH by Y_HEIGHT
        # py.draw.rect(surface, (255,255,255), (self.x * X_WIDTH + self.GRID_BORDER_WIDTH, self.y * Y_HEIGHT + self.GRID_BORDER_WIDTH, 
        #                                       X_WIDTH- self.GRID_BORDER_WIDTH, Y_HEIGHT- self.GRID_BORDER_WIDTH))

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 1:
                    py.draw.rect(surface, self.color, ((self.x + j) * X_WIDTH + self.GRID_BORDER_WIDTH, (self.y + i) * Y_HEIGHT + self.GRID_BORDER_WIDTH,
                                                       X_WIDTH - self.GRID_BORDER_WIDTH, Y_HEIGHT - self.GRID_BORDER_WIDTH))


class BoardTile():
    def __init__(self, is_set: bool, x: int, y: int, color: tuple) -> None:
        self.is_set = is_set
        self.x = x
        self.y = y
        self.color = color


class Board():
    def __init__(self, num_rows: int, num_cols: int, grid_border_width: int) -> None:
        self.NUM_ROWS = num_rows
        self.NUM_COLS = num_cols
        self.GRID_BORDER_WIDTH = grid_border_width
        self.grid = [[BoardTile(False, i, j, (0,0,0)) for i in range(1, num_cols + 1)] for j in range(1, num_rows + 1)]

    #print board to stdout
    def printBoard(self):
        for row in self.grid:
            print(row)

    def draw(self, surface: py.Surface) -> None:
        X_WIDTH = surface.get_width() / self.NUM_COLS
        Y_HEIGHT = surface.get_height() / self.NUM_ROWS

        for row in self.grid:
            for tile in row:
                if tile.is_set:
                    py.draw.rect(surface, tile.color, (tile.x * X_WIDTH + self.GRID_BORDER_WIDTH, tile.y * Y_HEIGHT + self.GRID_BORDER_WIDTH,
                                                       X_WIDTH - self.GRID_BORDER_WIDTH, Y_HEIGHT - self.GRID_BORDER_WIDTH))

    def movePieceDown(self) -> None:

        # check if peice has collided with another peice or the bottom of the board
        # if it has then set the peice to placed and create a new peice

        hit_bottom = self.get_current_piece().movedown()

        if hit_bottom:
            #put data into grid
            for i in range(len(self.get_current_piece().matrix)):
                for j in range(len(self.get_current_piece().matrix[i])):
                    if self.get_current_piece().matrix[i][j] == 1:
                        self.grid[self.get_current_piece().y + i][self.get_current_piece().x + j].is_set = True
                        self.grid[self.get_current_piece().y + i][self.get_current_piece().x + j].color = self.get_current_piece().color

            # create new peice
            self.set_current_piece(Piece(self.NUM_ROWS, self.NUM_COLS, self.GRID_BORDER_WIDTH))

        '''
        piece_set = False
        if deltamovespeed >= movespeed:
            piece_set = board.get_current_piece().movedown()
            deltamovespeed = 0
        else:
            deltamovespeed += dt
        
        if piece_set:
            board.set_current_piece(Piece(NUM_ROWS, NUM_COLS, GRID_BORDER_WIDTH))
        '''

    # getters and setters for current peice
    def get_current_piece(self) -> Piece:
        return self.__current_piece
    
    def set_current_piece(self, piece: Piece) -> None:
        self.__current_piece = piece

        # need to save the piece in the grid using matrix in peice

        #then need to check if their is a full row and remove it


