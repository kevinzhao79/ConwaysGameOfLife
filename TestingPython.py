"""
This program is designed to model and simulate 
John Conway's Game of Life through Python's tkinter GUI.
@author Kevin Zhao
"""

from tkinter import *
from tkinter import ttk
import random
DEAD = 0     # brightness value for a dead cell
ALIVE = 255  # brightness value for an alive cell

#create the game board size through command line args, then display it
"""
A class modeling the game board in which the Game of Life will be played.
"""
class Board:

    board_generation = 0

    """
    Default constructor for a Board object.
    @param length the length of the board (x coordinate).
    @param width the width of the Board (y coordinate).
    @param board a 2D list representing the board, which is 
           initialized to have all cells begin DEAD.
    """
    def __init__(self, length, width):
        self.length = length
        self.width = width
        board = [self.length, self.width]
        for i in range(0, self.length):
            for j in range(0, self.width):
                board[i,j] = Cell(DEAD, i, j)

    def get_board(self):
        return self.board
    
    """
    Randomizes the board's cells to either DEAD or ALIVE.
    @param frequency the frequency of cells that become ALIVE.
    """
    def randomize(self, frequency):
        if frequency < 0: frequency = 0
        if frequency > 1: frequency = 1
        for i in range(0, self.length):
            for j in range(0, self.width):
                if random(0,1) < frequency: self.board[i,j].set_state(self, ALIVE)

    """
    Updates the board to its next generation, using the following rules:
    1. If a DEAD cell is neighboring 3 ALIVE cells, it becomes ALIVE.
    2. If an ALIVE cell is neighboring 2 or 3 ALIVE cells, it stays ALIVE.
    3. If an ALIVE cell is neighboring 1 or less ALIVE cells, it becomes DEAD.
    4. If an ALIVE cell is neighboring 4 or more ALIVE cells, it becomes DEAD.
    """
    def update_board(self):
        copy_board = self.board.copy

        # iterate through every cell in the original board and determine
        # if it will be alive or dead in its next generation

        for i in range(0, self.length):
            for j in range(0, self.width):
                num_alive_neighbors = 0
                if i-1 >= 0 and j-1 >= 0: 
                    if self.board[i-1][j-1].get_state() == ALIVE: num_alive_neighbors += 1
                if i >= 0 and j-1 >= 0:
                    if self.board[i][j-1].get_state() == ALIVE: num_alive_neighbors += 1
                if i+1 <= self.length and j-1 >= 0:
                    if self.board[i+1][j-1].get_state() == ALIVE: num_alive_neighbors += 1
                if i-1 >= 0 and j >= 0:
                    if self.board[i-1][j].get_state() == ALIVE: num_alive_neighbors += 1
                if i+1 <= self.length and j >= 0:
                    if self.board[i+1][j].get_state() == ALIVE: num_alive_neighbors += 1
                if i-1 >= 0 and j+1 <= self.width: 
                    if self.board[i-1][j+1].get_state() == ALIVE: num_alive_neighbors += 1
                if i >= 0 and j+1 <= self.width:
                    if self.board[i][j+1].get_state == ALIVE: num_alive_neighbors += 1
                if i+1 <= self.length and j+1 <= self.width:
                    if self.board[i+1][j+1].get_state == ALIVE: num_alive_neighbors += 1
                
                # rule 1
                if self.board[i][j].get_state() == DEAD and num_alive_neighbors == 3: copy_board[i][j].set_state(ALIVE)

                # rule 2
                if self.board[i][j].get_state() == ALIVE and (num_alive_neighbors == 2 or num_alive_neighbors == 3): copy_board[i][j].set_state(ALIVE)

                # rule 3
                if self.board[i][j].get_state() == ALIVE and num_alive_neighbors < 2: copy_board[i][j].set_state(DEAD)

                # rule 4
                if self.board[i][j].get_state() == ALIVE and num_alive_neighbors > 3: copy_board[i][j].set_state(DEAD)

        self.board_generation += 1
        return copy_board
        
    """
    Resets the board such that all cells within the board are DEAD, and resets the board's generation.
    """
    def reset(self):
        for i in range(0, self.length):
            for j in range(0, self.width):
                self.board[i][j].set_state(DEAD)
        
        self.board_generation = 0

"""
A class modeling the cells within the Game of Life.
"""
class Cell:

    """
    Default constructor for a Cell object.
    @param state the state of the Cell, initialized to DEAD.
    @param x the x-coordinate within the Board.
    @param y the y-coordinate within the Board.
    """
    def __init__(self, state, x, y):
        state = DEAD
        self.x = x
        self.y = y

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def swap_state(self):
        if self.state == DEAD:
            self.state = ALIVE
        if self.state == ALIVE:
            self.state = DEAD

    def get_x(self):
        return self.x
    
    def set_x(self, x):
        self.x = x

    def get_y(self):
        return self.y

    def set_y(self, y):
        self.y = y

"""
The driver class for the simulation.
"""
class Main:
    pass