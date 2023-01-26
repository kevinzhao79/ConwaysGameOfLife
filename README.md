# ConwaysGameOfLife
Conway's Game of Life is a zero-player game created by mathematician John Conway. It is played on an infinite 2-Dimensional grid occupied by cells. Each cell has two states: DEAD and ALIVE. Each arrangement of cells is considered one 'generation', and each generation dictates its next generation according to these rules: 

1. If a DEAD cell is neighboring 3 ALIVE cells, it becomes ALIVE.
2. If an ALIVE cell is neighboring 2 or 3 ALIVE cells, it stays ALIVE.
3. If an ALIVE cell is neighboring 1 or less ALIVE cells, it becomes DEAD.
4. If an ALIVE cell is neighboring 4 or more ALIVE cells, it becomes DEAD.

Despite such simple rules, this game is one of many processes which are undecideable -- that is, given any one generation, it is impossible to tell whether or not that generation will dissolve or continue throughout infinitely many future generations. 

This is a short sandbox application which simulates Conway's Game of Life, created in Python 3.10.4 with its tkinter GUI by Kevin Zhao.
