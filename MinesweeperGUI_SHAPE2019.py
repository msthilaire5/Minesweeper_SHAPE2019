#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 14:49:58 2019

@author: msthilaire
"""

# For random coords of mine locations
import random
# For pretty display of gameboard list of lists
from pprint import pprint
# For keeping track of time to solve board
import time
# For GUI!
from tkinter import Tk, Label, Button, Frame, Canvas

def create_board(width, height):
    """
    This function creates a new blank gameboard filled with None values.
    @param width the number of columns gameboard will have
    @param height the number of rows gameboard will have
    @return the blank gameboard filled with None values
    """
    board = [] # final gameboard to return
    
    for row in range(0,height):
        row_li = [] # make new inner list of None's and adds to gameboard
        for col in range(0,width):
            row_li.append(None)
        board.append(row_li)
    
    return board


def bury_mines(gameboard,n):
    """
    This function buries mines at random locations on a gameboard.
    @param gameboard the gameboard to bury mines in
    @param n the number of mines to bury
    """
    # keep track of how many mines we've buried so far
    mines_buried = 0
    while (mines_buried < n):
        # Generating random locations!
        poss_row = random.randrange(0, len(gameboard))
        poss_col = random.randrange(0,len(gameboard[0]))
        # Make sure unique locat b4 dropping mine
        if gameboard[poss_row][poss_col] == None: # OK to drop!!!
            gameboard[poss_row][poss_col] = -1
            mines_buried += 1


def get_mine_count(gameboard, x, y):
    """
    This function counts how many mines are in the cells adjacent to the cell 
    whose coordinates are given.
    @param gameboard the gameboard with the cell in question
    @param x the col number of the cell in question
    @param y the row number of the cell in question
    @return the number of mines adjacent to the cell denoted by x and y
    """
    mine_count = 0
    height = len(gameboard)
    width = len(gameboard[0])
    
    # Checking all directions to see which possible, prev IndexErrors!
    upOK = y > 0 # Won't go for [-1]
    downOK = (y + 1 < height) # Won't try to access nonexistent index
    leftOK = x > 0
    rightOK = (x + 1 < width)
    
    # Up
    if upOK and (gameboard[y-1][x] == -1):
        mine_count += 1
    # Down
    if downOK and (gameboard[y+1][x] == -1):
        mine_count += 1
    # Left
    if leftOK and (gameboard[y][x-1] == -1):
        mine_count += 1
    # Right
    if rightOK and (gameboard[y][x+1] == -1):
        mine_count += 1
    # Northwest!
    if leftOK and upOK and (gameboard[y-1][x-1] == -1):
        mine_count += 1
    # Northeast!
    if rightOK and upOK and (gameboard[y-1][x+1] == -1):
        mine_count += 1
    # Southwest!
    if leftOK and downOK and (gameboard[y+1][x-1] == -1):
        mine_count += 1
    # Southeast!
    if rightOK and downOK and (gameboard[y+1][x+1] == -1):
        mine_count += 1
    
    return mine_count


def print_mines(gameboard):
    """
    This function prints the board, only indicating the location of mines with *.
    @param gameboard the gameboard to display
    """
    # Making col number string
    # 3 leading spaces for two-digit num and |
    col_header = "   "
    for col in range(0, len(gameboard[0])):
        col_header += ("{:^4s}".format(str(col)))
    print(col_header)
    # Dashed line separator
    print("   " + ("-" * (len(col_header) - 3)))
    
    # want to print mine locats line-by-line
    for row in range(0,len(gameboard)):
        row_str = "{:>2s}|".format(str(row))
        for col in range(0,len(gameboard[0])):
            if gameboard[row][col] == -1: # Mine locat!!!
                row_str += "{:^4s}".format("*")
            else: # No mine, probably None
                row_str += "{:^4s}".format(".")
        print(row_str)
    

def print_board(gameboard):
    """
    This function prints the board, indicating mine locations with * and cells 
    that have mines adjacent to them with the number of adjacent mines.
    @param gameboard the gameboard to display
    """
    # Making col number string
    # 3 leading spaces for two-digit num and |
    col_header = "   "
    for col in range(0, len(gameboard[0])):
        col_header += ("{:^4s}".format(str(col)))
    print(col_header)
    # Dashed line separator
    print("   " + ("-" * (len(col_header) - 3)))
    
    # want to print locats line-by-line
    for row in range(0,len(gameboard)):
        row_str = "{:>2s}|".format(str(row))
        for col in range(0,len(gameboard[0])):
            if gameboard[row][col] == -1: # Mine locat!!!
                row_str += "{:^4s}".format("*")
            else: # No mine, probably None
                row_str += "{:^4d}".format(get_mine_count(gameboard, col, row))
        print(row_str)


def user_view(gameboard):
    """
    This function displays the board as it is seen by the user.
        - '.' if discovered with 0 adjacent mines
        - '?' if undiscovered with None or a mine
        - a positive int if discovered with adjacent mines
    @param gameboard the gameboard to display
    """
    
    # Making col number string
    # 3 leading spaces for two-digit num and |
    col_header = "   "
    for col in range(0, len(gameboard[0])):
        col_header += ("{:^4s}".format(str(col)))
    print(col_header)
    # Dashed line separator
    print("   " + ("-" * (len(col_header) - 3)))
    
    # want to print locats line-by-line
    for row in range(0,len(gameboard)):
        row_str = "{:>2s}|".format(str(row))
        for col in range(0,len(gameboard[0])):
            if (gameboard[row][col] == -1) or (gameboard[row][col] == None): # Mine locat or None, undiscovered!!!
                row_str += "{:^4s}".format("?")
            elif (gameboard[row][col] == 0): # Discovered, no adjacent mines
                row_str += "{:^4s}".format(".")
            else: # Discovered, yes adjacent mines
                row_str += "{:^4d}".format(gameboard[row][col])
        print(row_str)
        

def uncover_board(gameboard, x, y):
    """
    'CASCADING ALGORITHM'
    This function uncovers cells on the board. Reveals whether they are mines,
    empty, or have mines adjacent to them.
    @param gameboard the gameboard whose cells will be uncovered
    @param x the column of the cell to uncover
    @param y the row of the cell to uncover
    """
    if gameboard[y][x] in [-1, None]: # Still undiscovered, not a mine!
        adj_mines = get_mine_count(gameboard,x,y)
        # Cell has no adjacent mines!
        if adj_mines == 0:
            gameboard[y][x] = 0
            # Uncover all adjacent cells!!!
            
            height = len(gameboard)
            width = len(gameboard[0])
            # Checking all directions to see which possible, prev IndexErrors!
            upOK = y > 0 # Won't go for [-1]
            downOK = (y + 1 < height) # Won't try to access nonexistent index
            leftOK = x > 0
            rightOK = (x + 1 < width)
            
            # Up
            if upOK:
                uncover_board(gameboard, x, y-1)
            # Down
            if downOK:
                uncover_board(gameboard, x, y+1)
            # Left
            if leftOK:
                uncover_board(gameboard, x-1, y)
            # Right
            if rightOK:
                uncover_board(gameboard, x+1, y)
            # Northwest!
            if leftOK and upOK:
                uncover_board(gameboard, x-1, y-1)
            # Northeast!
            if rightOK and upOK:
                uncover_board(gameboard, x+1, y-1)
            # Southwest!
            if leftOK and downOK:
                uncover_board(gameboard, x-1, y+1)
            # Southeast!
            if rightOK and downOK:
                uncover_board(gameboard, x+1, y+1)
            
        # Cell has adjacent mines
        elif adj_mines > 0: 
            gameboard[y][x] = adj_mines


def check_won(gameboard):
    
    no_None = True
    row = 0
    # Go row-by-row and see if any None vals left
    while no_None and row < len(gameboard):
        if None in gameboard[row]:
            no_None = False
        row += 1
    return no_None


def display_board(board, canvas):
    widthpxl = len(board[0]) * 31
    heightpxl = len(board) * 31
    print(widthpxl)
    print(heightpxl)
    
    for canvas_y in range(0,heightpxl,31):
        row = canvas_y // 31
        for canvas_x in range(0,widthpxl,31):
            col = canvas_x // 31
            # Cell content
            cell_text = ''
            if board[row][col] == -1 or board[row][col] == None: # Undiscovered, maybe mine locat
                cell_color = 'grey'
            elif board[row][col] == 0: # Discovered, no mines or adjacent ones
                cell_color = 'light grey'
            else: # Discovered, yes adjacent mines
                cell_color = 'yellow'
                cell_text = str(board[row][col])
            # Cell appearance
            canvas.create_rectangle(canvas_x, canvas_y, (canvas_x + 30), (canvas_y + 30), fill=cell_color)
            if cell_text != '':
                canvas.create_text(canvas_x + 15, canvas_y + 15, font="arial 20", text=cell_text)
            
            

# GUI FUNCTION!!!!!!!!!
def run_gui():
    """
    This function runs the GUI version of minesweeper.
    """
    # Gboard creation
    print("Creating your gameboard...")
    gboard = create_board(10, 10)
    # Burying mines
    print("Burying mines...")
    bury_mines(gboard, 20)
    print_board(gboard)
    
    # Creating window
    root = Tk()
    root.wm_title("Minesweeper")
    # Prep for canvas widget
    heightpxl = (len(gboard) * 31)
    print(heightpxl)
    widthpxl = (len(gboard[0]) * 31)
    print(widthpxl)
    canvas = Canvas(master=root,height=heightpxl,width=widthpxl)
    canvas.pack()
    
    # Set up window
    display_board(gboard,canvas) 
    
    
    # Set-up for event handler
    def handle_click(event):
        # Pull coords of click and translate to row/col
        x = event.x // 31
        y = event.y // 31
        print("Coords: {}, {}".format(x,y))
        if gboard[y][x] == -1: 
            print("GAME OVER!!!")
            gboard[y][x] = chr(9760)
            canvas.unbind("<Button-1>")
        else:
            # Change gboard val
            uncover_board(gboard, x, y)
        # Update view
        display_board(gboard,canvas)
        # Check if won
        if check_won(gboard):
            print("YAY!!! YOU WON!!!")
            canvas.unbind("<Button-1>")

    
    # Binding event handler to canvas widget
    canvas.bind("<Button-1>", handle_click)
    # Display the window now!!
    root.mainloop()
    
run_gui()
print("Game closed.")