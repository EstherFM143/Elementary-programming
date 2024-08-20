# Elementary-programming
MINESWEEPER.
Welcome to Minesweeper game. My final assignment for elementary programming course at University of Oulu is to develop a minesweeper game using Python programming language, and the library (sweeperlib.py) and graphics (sprites.zip) provided.

Game Setup.
The minefield is a two-dimensional, rectangular grid containing mines. The player can determine the dimensions of the field and the number of mines. All tiles are initially unrevealed, with mines randomly placed. The tiles can be:
Mine tiles: End the game if clicked.
Number tiles: Show the number of adjacent mines.
Empty tiles: Trigger a chain reaction of revealing adjacent tiles until a number tile is encountered.

Gameplay.
Tile Selection: Click a tile to reveal its content.
If it contains a mine, the game is over.
If it contains a number, the number of adjacent mines is displayed.
If it is empty, all adjacent tiles are revealed recursively until a number tile is encountered.
Game End: The game ends when either a mine is clicked (loss) or all non-mine tiles are revealed (win).

Further instructions of the assignment can be seen in instructions.pdf
