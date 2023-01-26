"""
This program is designed to model and simulate 
John Conway's Game of Life through Python's tkinter GUI.
@author Kevin Zhao
"""

from tkinter import *
from tkinter import ttk
import random
import time
import copy
DEAD = '#000000'       # hex value for black, representing a dead cell
ALIVE = '#FFFFFF'      # hex value for white, representing an alive cell
board_generation = 0  # number of generations the game board has gone through

"""
A class modeling the game board in which the Game of Life will be played.
"""
class Board:

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
        self.board_generation = 0
        self.board = []
        for i in range(self.length):
            temp = []
            for j in range(self.width):
                temp.append(Cell(i, j))
            self.board.append(temp)
    
    """
    Randomizes the board's cells to either DEAD or ALIVE.
    @param frequency the frequency of cells that become ALIVE.
    """
    def randomize(self, frequency):
        if frequency < 0: frequency = 0
        if frequency > 1: frequency = 1
        for i in range(0, self.length):
            for j in range(0, self.width):
                if random.random() < frequency: self.board[i][j].state = ALIVE

    """
    Updates the board to its next generation, using the following rules:
    1. If a DEAD cell is neighboring 3 ALIVE cells, it becomes ALIVE.
    2. If an ALIVE cell is neighboring 2 or 3 ALIVE cells, it stays ALIVE.
    3. If an ALIVE cell is neighboring 1 or less ALIVE cells, it becomes DEAD.
    4. If an ALIVE cell is neighboring 4 or more ALIVE cells, it becomes DEAD.
    """
    def update_board(self):
        def valid_and_alive_cell(i, j):
            if i >= 0 and i < self.length and j >= 0 and j < self.width and self.board[i][j].state == ALIVE:
                return True
            return False
        copy_board = copy.deepcopy(self.board)

        # iterate through every cell in the original board and determine
        # if it will be alive or dead in its next generation
        for i in range (0, self.length):
            for j in range  (0, self.width):
                # check each cell's neighbors and tally how many of those neighbors are alive
                num_alive_neighbors = 0
                # check the cell's neighbors
                for di in (-1, 0, 1):
                    for dj in (-1, 0, 1):
                        # not including itself
                        if not (di == 0 and dj == 0):
                            if valid_and_alive_cell(i + di, j + dj):
                                num_alive_neighbors += 1
                
                # use the cell's status and its number of alive neighbors to determine its updated status

                # rule 1
                if self.board[i][j].state == DEAD and num_alive_neighbors == 3: copy_board[i][j].state = ALIVE

                # rule 2
                elif self.board[i][j].state == ALIVE and (num_alive_neighbors == 2 or num_alive_neighbors == 3): copy_board[i][j].state = ALIVE

                # rule 3
                elif self.board[i][j].state == ALIVE and num_alive_neighbors < 2: copy_board[i][j].state = DEAD

                # rule 4
                elif self.board[i][j].state == ALIVE and num_alive_neighbors > 3: copy_board[i][j].state = DEAD

        self.board_generation += 1
        self.board = copy_board
        
    """
    Resets the board such that all cells within the board are DEAD, and resets the board's generation.
    """
    def reset(self):
        for i in range(0, self.length):
            for j in range(0, self.width):
                self.board[i][j].state = DEAD
        
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
    def __init__(self, x, y):
        self.state = DEAD
        self.x = x
        self.y = y

    """
    Swaps the state of the cell from DEAD -> ALIVE or ALIVE -> DEAD
    """
    def swap_state(self):
        if self.state == DEAD:
            self.state = ALIVE
        elif self.state == ALIVE:
            self.state = DEAD

"""
The driver function for the simulation.
"""
def main():

    # Creates the console and its frame.
    root = Tk()
    menu = ttk.Frame(root, padding=10)
    menu.grid()

    # Basic widgets for the frame.
    ttk.Label(menu, text = "Conway's Game of Life: A Simulation Sandbox").grid(column = 1, row = 0)
    ttk.Button(menu, text = "Quit the Simulation", command = menu.destroy).grid(column = 2, row = 3)
    game_board = Board(100, 100)
    game_board.randomize(0.2)

    # A canvas that displays the actual game board and the status of each of its cells.
    board_visual = Canvas(menu, width = 1000, height = 1000)
    board_visual.grid(column = 1, row = 1, rowspan = 100)

    # for each cell in the game board,
    def update_board_visual():
        for i in range(0, game_board.length):
            for j in range(0, game_board.width):

                # if the cell is alive, create a black square showing the cell is dead
                if game_board.board[i][j].state == DEAD:
                    board_visual.create_rectangle(i*10, j*10, (i+1)*10+1, (j+1)*10+1, fill = DEAD)

                # otherwise, create a white square showing the cell is alive
                elif game_board.board[i][j].state == ALIVE: 
                    board_visual.create_rectangle(i*10, j*10, (i+1)*10+1, (j+1)*10+1, fill = ALIVE)

    def show_generation_tally():
        generation_tally = ttk.Label(menu, text = "Current Board Generation: " + str(game_board.board_generation))
        generation_tally.grid(column = 2, row = 1)

    def update_board_handler():
        game_board.update_board()
        update_board_visual()
        show_generation_tally()
        
    def reset_board_handler(): 
        game_board.reset()
        update_board_visual()
        game_board.board_generation = 0
        show_generation_tally()

    def randomize_board_handler():
        game_board.reset()
        game_board.randomize(frequency_entry.get())
        update_board_visual()
        show_generation_tally()

    # A sliding scale that can adjust the frequency of alive cells in the simulation.
    frequency_entry = Scale(menu, from_ = 0.000, to = 1.000, label = "Frequency", resolution = 0.001, tickinterval = 0.1, length = 250)
    frequency_entry.grid(column = 0, row = 3)

    # Creates the game board, which will update after each generation.
    generate_board = ttk.Button(menu, text = "Generate New Simulation", command = randomize_board_handler)
    generate_board.grid(column = 0, row = 2)

    # Resets the game board to all dead cells.
    reset_board = ttk.Button(menu, text = "Reset Simulation", command = reset_board_handler)
    reset_board.grid(column = 0, row = 1)

    # Finds the current board's next generation, and displays that on the console.
    next_generation = ttk.Button(menu, text = "Next Generation", command = update_board_handler)
    next_generation.grid(column = 2, row = 2)

    # initial visuals for the current board and its generation tally
    update_board_visual()
    show_generation_tally()

    menu.mainloop()

main()