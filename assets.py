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
        self.x = 5
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

    # def rotate_90(self):
    #     self.matrix = [list(reversed(row)) for row in zip(*self.matrix)]
    
    # def rotate_90_counterclockwise(self):
    #     self.matrix = [list(row) for row in zip(*reversed(self.matrix))]

    # def movedown(self) -> bool:
    #     self.y += 1
    
    # def moveleft(self) -> None:
    #     self.x -= 1
    
    # def moveright(self) -> None:
    #     self.x += 1


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
        self.grid = [[BoardTile(False, i, j, (0,0,0)) for i in range(num_cols)] for j in range(num_rows)]

        

    #print board to stdout
    def printBoard(self) -> None:
        for row in self.grid:
            print(row)

    def draw(self, surface: py.Surface) -> None:
        X_WIDTH = surface.get_width() / self.NUM_COLS
        Y_HEIGHT = surface.get_height() / self.NUM_ROWS

        #draw border of placed tiles
        for row in self.grid:
            for tile in row:
                if tile.is_set:
                    py.draw.rect(surface, tile.color, (tile.x * X_WIDTH + self.GRID_BORDER_WIDTH, tile.y * Y_HEIGHT + self.GRID_BORDER_WIDTH,
                                                       X_WIDTH - self.GRID_BORDER_WIDTH, Y_HEIGHT - self.GRID_BORDER_WIDTH))
                    
        #draw active tile
        for i in range(len(self.active_piece().matrix)):
            for j in range(len(self.active_piece().matrix[i])):
                if self.active_piece().matrix[i][j] == 1:
                    py.draw.rect(surface, self.active_piece().color, ((self.active_piece().x + j) * X_WIDTH + self.GRID_BORDER_WIDTH, (self.active_piece().y + i) * Y_HEIGHT + self.GRID_BORDER_WIDTH,
                                                       X_WIDTH - self.GRID_BORDER_WIDTH, Y_HEIGHT - self.GRID_BORDER_WIDTH))

    def checkCollision(self, x: int, y: int, matrix: list) -> bool:
        
        #check if piece is out of bounds
        if x < 0 or x + len(matrix) > self.NUM_COLS:
            return True
        if y < 0 or y + len(matrix) > self.NUM_ROWS:
            return True

        #check if piece is colliding with another piece
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 1 and self.grid[y + i][x + j].is_set:
                    return True
        
        return False
    
    def rotate_90(self):
        newMatrix = [list(reversed(row)) for row in zip(*self.active_piece().matrix)]

        if self.checkCollision(self.active_piece().x, self.active_piece().y, newMatrix):
            return

        self.active_piece().matrix = newMatrix
    
    def rotate_90_counterclockwise(self):

        newMatrix = [list(row) for row in zip(*reversed(self.active_piece().matrix))]

        if self.checkCollision(self.active_piece().x, self.active_piece().y, newMatrix):
            return
        
        self.active_piece().matrix = newMatrix

    def movedown(self) -> None:

        if self.checkCollision(self.active_piece().x, self.active_piece().y + 1, self.active_piece().matrix):
            #place piece into grid
            for i in range(len(self.active_piece().matrix)):
                for j in range(len(self.active_piece().matrix[i])):
                    if self.active_piece().matrix[i][j] == 1:
                        self.grid[self.active_piece().y + i][self.active_piece().x + j].is_set = True
                        self.grid[self.active_piece().y + i][self.active_piece().x + j].color = self.active_piece().color

            # create new peice
            self.set_current_piece(Piece(self.NUM_ROWS, self.NUM_COLS, self.GRID_BORDER_WIDTH))
            return

        self.active_piece().y += 1
    
    def moveleft(self) -> None:

        if self.checkCollision(self.active_piece().x - 1, self.active_piece().y, self.active_piece().matrix):
            return

        self.active_piece().x -= 1
    
    def moveright(self) -> None:

        if self.checkCollision(self.active_piece().x + 1, self.active_piece().y, self.active_piece().matrix):
            return

        self.active_piece().x += 1
    
    # def movePieceDown(self) -> None:

    #     # check if peice has collided with another peice or the bottom of the board
    #     # if it has then set the peice to placed and create a new peice

    #     hit_bottom = self.active_piece().movedown()

    #     if hit_bottom:
    #         #put data into grid
    #         for i in range(len(self.active_piece().matrix)):
    #             for j in range(len(self.active_piece().matrix[i])):
    #                 if self.active_piece().matrix[i][j] == 1:
    #                     self.grid[self.active_piece().y + i][self.active_piece().x + j].is_set = True
    #                     self.grid[self.active_piece().y + i][self.active_piece().x + j].color = self.active_piece().color

    #         # create new peice
    #         self.set_current_piece(Piece(self.NUM_ROWS, self.NUM_COLS, self.GRID_BORDER_WIDTH))

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
    def active_piece(self) -> Piece:
        return self.__current_piece
    
    def set_current_piece(self, piece: Piece) -> None:
        self.__current_piece = piece

        # need to save the piece in the grid using matrix in peice

        #then need to check if their is a full row and remove it


