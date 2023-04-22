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
    def __init__(self, num_rows: int, num_cols: int, grid_width: int) -> None:
        self.type = PieceType(random.randint(1, 3))
        self.rotation = Rotation(random.randint(1, 4))
        self.x = 3
        self.y = 3
        self.matrix = []
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        self.NUM_ROWS = num_rows
        self.NUM_COLS = num_cols
        self.GRID_WIDTH = grid_width

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

    def movedown(self) -> None:
        self.y += 1
    
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
        py.draw.rect(surface, (255,255,255), (self.x * X_WIDTH + self.GRID_WIDTH, self.y * Y_HEIGHT + self.GRID_WIDTH, X_WIDTH- self.GRID_WIDTH, Y_HEIGHT- self.GRID_WIDTH))

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 1:
                    py.draw.rect(surface, self.color, ((self.x + j) * X_WIDTH + self.GRID_WIDTH, (self.y + i) * Y_HEIGHT + self.GRID_WIDTH,
                                                       X_WIDTH - self.GRID_WIDTH, Y_HEIGHT - self.GRID_WIDTH))