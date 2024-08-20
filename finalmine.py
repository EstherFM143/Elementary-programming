import time
import random
import sweeperlib

status = {
    "field": [],
    "visible_field": [],
    "shift_number": 0,
    "mines": 0
}

def platform_game(height, width, mines):
    """
    Initializes a platform game with a specified height, width, and number of mines.

    This function creates two fields: 
    the game field where the mines are placed 
    and the player's field which is visible to the player. 
    The mines are randomly placed on the game field using the `place_mines` function.
    """
    field = []        #initializes empty list for game field
    for row in range(height):
        field.append([])      #add empty list for each row
        for column in range(width):
            field[-1].append(" ")   #add space character to show empty cell
    status["field"] = field
                         # from exercise 4
    foot = []    #empty list to store coordinates of each cell
    for x in range(width):
        for y in range(height):
            foot.append((x, y))   #add coordinates of cell to the list

    visible_field = []        #same as field
    for row in range(height):
        visible_field.append([])
        for column in range(width):
            visible_field[-1].append(" ")
    status["visible_field"] = visible_field

    place_mines (field, foot, mines)   # Call the place_mines function
    return field, visible_field        #to place the mines on the field

def create_field():
    """
    A function that draws a field into a game window using sweeperlib. 
    This function is called whenever the game engine requests
    a screen update.
    """
    sweeperlib.clear_window()
    sweeperlib.draw_background()
    sweeperlib.begin_sprite_draw()
           # Loops through each tile in the visible field
    for height, row in enumerate(status["visible_field"]):
        for width, column in enumerate(row):
            y = height * 40     #calculate x-coord of the cell based on its row
            x = width * 40      #calculate y-coord of the cell based on its column
            sweeperlib.prepare_sprite(column, x, y)
        sweeperlib.draw_sprites()

def place_mines(field, foot, mines_number):
    """
    This function randomly creates mines on a field in random tiles.
    """
    mines = random.sample(foot, mines_number)
    for mine in mines:    #from ex 4
        x, y = mine
        field[y][x] = "x"
        foot.remove(mine)
        # Place a mine (represented as 'x') at the selected location on the field

def empty_squares():
    """
    This function calculates and returns the total number of empty squares in a given field.
    The field is obtaines from status dictionary. An empty square is defined as a square 
    that is either unvisited (" ") or flagged ("f")
    """
    field = status["visible_field"] #get the visible field from status dict
    empty = 0
    for i, row in enumerate(field):     #iterate over each row in the field
        empty_row = row.count(" ") + row.count("f")   #count no of empty&flagged squares
        empty += empty_row  #add the count to the total number of empty squares
    return empty

def adjacent_mines(x, y, field):
    """
    This function counts the number of mines adjacent to a given square in the field.
    """
    nomines = 0     #initial number of mines
     #Define the range of y-coordinates and x_coordinate to check
    y_limit = {y, y -1, y + 1}
    x_limit = {x, x - 1, x + 1}

    for y, row in enumerate(field):   # Iterate over each row in the field
        for x, box in enumerate(row):  # Iterate over each square in the row
            if y in y_limit and x in x_limit and box == "x": #Square within defined range&has mine
                nomines += 1  # add the count of adjacent mines
    return nomines

def minegate(field, visible_field, x, y):
    """
    This function handles opening of minefield tiles
    """
    field_height = len(field)  # Get the height of the field
    field_width = len(field[0])  # Get the width of the field
    number = adjacent_mines(x, y, field)  # Get the number of adjacent mines
    explore = [(x, y)]   # Initialize a list with the current position to explore

    while len(explore) > 0:
        x, y = explore.pop()   # Get the last position to explore
        if field[y][x] != "x":   # If the current position is not a mine
            number = adjacent_mines(x, y, field)
            if number > 0:      # If there are adjacent mines
                visible_field[y][x] = number    # Update the visible field with the no.mines
                field[y][x] = number            # update the actual field too
                continue
            else:
                visible_field[y][x] = "0"
                field[y][x] = "0"
        for i in range(y - 1, y + 2):       # For each row, then column in the adjacent positions
            for j in range(x - 1, x + 2):
                if i < field_height and i >= 0 and j < field_width and j >= 0:  #If position is within field
                    if visible_field[i][j] == " ":    # If the position is not yet visible
                        explore.append((j, i))  #Add position to the list of positions to explore

def move_mouse(x, y, button, editbutton):
    """
    This function handles where the user presses and does things depending on the button
    """
    right = sweeperlib.MOUSE_RIGHT
    left = sweeperlib.MOUSE_LEFT
    visible_field = status["visible_field"]
    field = status["field"]

#mine marking feature
    if button == right: # If the right mouse button is clicked
        x = int(x / 40) # calculate x and y-coordinate in the field
        y = int(y / 40)
        if visible_field[y][x] == " ":   # If the field is not yet visible
            visible_field[y][x] = "f"    # mark the field as flagged
        elif visible_field[y][x] == "f":  # if the field is flagged
            visible_field[y][x] = " "     # unflag the field

#selecting boxes and marking win/loss
    if button == left:
        x = int(x / 40)
        y = int(y / 40)
        if field[y][x] == " ":   # If the field is empty, mark it as empty
            field[y][x] = "0"
            visible_field[y][x] = "0"  # make the field visible
            minegate(field, visible_field, x, y)  # Open the surrounding tiles
            status["shift_number"] += 1    # Increase the turn number
            if empty_squares() == status["mines"]:
                print("Well done!You won the game!")
                status["result"] = "win"   #mark game as won
                sweeperlib.close()

        elif field[y][x] == "x":   #if field is a mine, make mine visible
            visible_field[y][x] = "x"
            sweeperlib.draw_sprites()  #draw the sprites then increase the turn number
            status["shift_number"] += 1
            print("You blew up a mine! Better luck next time!")
            status["result"] = "loss"
            sweeperlib.close()

def statistics_recording(date, starttime, endtime, result, height, width, mines, shift_number):
    """
    Save game results to a text file
    """
    if endtime >= starttime:  #both from recorded time(time.localtime)
        game_duration = endtime - starttime
    else:
        game_duration = 60 - starttime + endtime
    with open("results.txt", "a", encoding='utf-8') as r:
        r.write(f"Date: {date}.\n Final score: {result}\n Game play_duration: {game_duration}.\n"
        f" Number of turns: {shift_number}.\n Playfield size: {width} x {height}\n Mines: {mines}\n")

def statistics_print():
    """
    Print statistics from the text file in which they were saved
    """
    with open("results.txt", "r", encoding='utf-8') as file:
        print(file.read())

def main():
    """
    Loads the game graphics, creates a game window, and sets a draw handler.
    The function validates the user's input for the field dimensions
    and the number of mines. It also handles the game's sprites, 
    window creation, mouse handling, records the game statistics and game start. 
    The function is designed to be run in a loop until the user chooses to quit.
    """

    print("_____WELCOME TO MINESWEEPER GAME_____")
    print("(1) Start a new game")
    print("(2) View statistics")
    print("(3) Quit")
    menu = int(input("Choose an option, (1), (2) or (3)"))
    while True:
        if menu == 1:
            height = int(input("Set height of field: "))
            width = int(input("Set width of field: "))
            try:
                if width < 2 or height < 2:
                    print("Very small dimensions! Not possible!")
                    break
            except ValueError:
                print("Use only integers!")
            try:
                mines = int(input("Enter the number of mines: "))
                status["mines"] = mines
                if mines < 1:
                    print("You can't play without mines!")
                    break
                if mines >= height * width:
                    print("Too many mines to fit the field!")
                    break
            except ValueError:
                print("Use only integers!")
                break
            status["shift_number"] = 0
            date = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
            starttime = time.localtime().tm_min #record start time for game duration
            sweeperlib.load_sprites("sprites")
            sweeperlib.create_window(width * 40, height * 40)
            platform_game(height, width, mines)
            sweeperlib.set_draw_handler(create_field)
            sweeperlib.set_mouse_handler(move_mouse)
            sweeperlib.start()
            endtime = time.localtime().tm_min   #end time for game duration
            statistics_recording(date, starttime, endtime, status["result"], height, width, mines, status["shift_number"])
            return
        elif menu == 2:
            statistics_print()
            return
        elif menu == 3:
            quit()
        else:
            print("Choose one of the given options! Just a number!")
            return

if __name__ == "__main__":
    while True:
        main()
