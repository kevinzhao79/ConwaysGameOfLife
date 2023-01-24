"""
This program is designed to model and simulate 
John Conway's Game of Life through Python's tkinter GUI.
@author Kevin Zhao
"""

from tkinter import *
from tkinter import ttk
import random
DEAD = '000000'       # hex value for black, representing a dead cell
ALIVE = 'FFFFFF'      # hex value for white, representing an alive cell
board_generation = 0  # number of generations the game board has gone through

#create the game board size through command line args, then display it
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
        board = [self.length, self.width]
        for i in range(0, self.length):
            for j in range(0, self.width):
                board[i,j] = Cell(DEAD, i, j)

    """
    Returns the board.
    @return the board.
    """
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
    @return the updated board.
    """
    def update_board(self):
        copy_board = self.board.copy

        # iterate through every cell in the original board and determine
        # if it will be alive or dead in its next generation
        for i in range(0, self.length):
            for j in range(0, self.width):

                # check each cell's neighbors and tally how many of those neighbors are alive
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
                
                # use the cell's status and its number of alive neighbors to determine its updated status

                # rule 1
                if self.board[i][j].get_state() == DEAD and num_alive_neighbors == 3: copy_board[i][j].set_state(ALIVE)

                # rule 2
                elif self.board[i][j].get_state() == ALIVE and (num_alive_neighbors == 2 or num_alive_neighbors == 3): copy_board[i][j].set_state(ALIVE)

                # rule 3
                elif self.board[i][j].get_state() == ALIVE and num_alive_neighbors < 2: copy_board[i][j].set_state(DEAD)

                # rule 4
                elif self.board[i][j].get_state() == ALIVE and num_alive_neighbors > 3: copy_board[i][j].set_state(DEAD)

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
    Generates a new board based on its inputs:
    @param length the length of the new board.
    @param width the width of the new board.
    @param frequency the frequency of ALIVE cells on the new board.
    """
    def generate_board(self, length, width, frequency):
        self.length = length
        self.width = width
        self.randomize(frequency)
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
        elif self.state == ALIVE:
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

    # Creates the console and its frame.
    root = Tk()
    menu = ttk.Frame(root, padding=10)
    menu.grid()

    # Basic widgets for the frame.
    ttk.Label(menu, text = "Conway's Game of Life: A Simulation Sandbox").grid(column = 0, row = 0)
    ttk.Button(menu, text = "Quit the Simulation", command = menu.destroy).grid(column = 5, row = 5)
    game_board = Board.__init__(Board, 1, 1)

    # Creates entry widgets to get the user's specified length and width of the game board.
    length_entry_label = ttk.Label(menu, text = "Length of Board (0 - 100)")
    l = StringVar("100")
    length_dim_entry = ttk.Entry(menu, textvariable = l)
    length_dim_entry.grid(column = 1, row = 0)

    width_entry_label = ttk.Label(menu, text = "Width of Board(0 - 100)")
    w = StringVar("100")
    width_dim_entry = ttk.Entry(menu, textvariable = w)
    width_dim_entry.grid(column = 1, row = 1)

    # Creates a checkbox widget to check if the user wants to create a random arrangement of alive and dead
    # cells on the game board; if the user ticks the box, it will prompt the user to enter a frequency for
    # the frequency of alive cells proportional to the total number of cells in the board.
    r = BooleanVar(FALSE)
    random_check = ttk.Checkbutton(menu, text = "Random Arrangement?", textvariable = r)
    random_check.grid(column = 2, row = 0)

    f = DoubleVar(0.0)
    frequency_entry = ttk.Entry(menu, text = "Frequency of Alive Cells (0.00 - 1.00)", textvariable = f)
    frequency_entry.grid(column = 2, row = 1)

    # Creates the game board, which will update after each generation.
    generate_board = ttk.Button(menu, text = "Generate Board", command = game_board.generate_board(l, w, f))

    # A canvas that displays the actual game board and the status of each of its cells.
    board_visual = Canvas(menu, width = 1000, height = 1000)

    # for each cell in the game board,
    for i in range(0, l):
        for j in range(0, w):

            # if the cell is alive, create a black square showing the cell is dead
            if game_board[i][j].get_state() == DEAD:
                board_visual.create_rectangle(i*10, j*10, (i+1)*10+1, (j+1)*10+1, fill = DEAD)

            # otherwise, create a white square showing the cell is alive
            elif game_board[i][j].get_state() == ALIVE: 
                board_visual.create_rectangle(i*10, j*10, (i+1)*10+1, (j+1)*10+1, fill = ALIVE)


    # Allows the user to show and hide the game board.
    show_board = ttk.Button(menu, text = "Show Board")

    # Resets the game board to all dead cells.
    reset_board = ttk.Button(menu, text = "Reset Simulation", command = game_board.reset())

    # Finds the current board's next generation, and displays that on the console.
    next_generation = ttk.Button(menu, text = "Next Generation", command = game_board.update_board())

    # A tally to keep track of the number of generations that have elapsed.
    generation_tally = ttk.Label(menu, text = board_generation)

    menu.mainloop()