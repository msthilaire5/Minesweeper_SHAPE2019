#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 17:02:04 2019

@author: msthilaire
"""

# For random coords of mine locations
import random
# For pretty display of gameboard list of lists
from pprint import pprint
# For keeping track of time to solve board
import time
import copy

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
    if upOK and (gameboard[y-1][x] == -1 or gameboard[y-1][x] == 'X'):
        mine_count += 1
    # Down
    if downOK and (gameboard[y+1][x] == -1 or gameboard[y+1][x] == 'X'):
        mine_count += 1
    # Left
    if leftOK and (gameboard[y][x-1] == -1 or gameboard[y][x-1] == 'X'):
        mine_count += 1
    # Right
    if rightOK and (gameboard[y][x+1] == -1 or gameboard[y][x+1] == 'X'):
        mine_count += 1
    # Northwest!
    if leftOK and upOK and (gameboard[y-1][x-1] == -1 or gameboard[y-1][x-1] == 'X'):
        mine_count += 1
    # Northeast!
    if rightOK and upOK and (gameboard[y-1][x+1] == -1 or gameboard[y-1][x+1] == 'X'):
        mine_count += 1
    # Southwest!
    if leftOK and downOK and (gameboard[y+1][x-1] == -1 or gameboard[y+1][x-1] == 'X'):
        mine_count += 1
    # Southeast!
    if rightOK and downOK and (gameboard[y+1][x+1] == -1 or gameboard[y+1][x+1] == 'X'):
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
            elif (gameboard[row][col] == 'X' or gameboard[row][col] == 'x'): # flagged!
                row_str += "{:^4s}".format(chr(9873))
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
    """
    This function checks if the user won Minesweeper by making sure there aren't
    any None values left.
    @param gameboard the gameboard to check if the user won
    """
    
    no_None = True
    row = 0
    # Go row-by-row and see if any None vals left
    while no_None and row < len(gameboard):
        if None in gameboard[row] or 'x' in gameboard[row]:
            no_None = False
        row += 1
    return no_None


def place_flag(gameboard, orig_val_dict, x, y):
    """
    This function places/removes flags on the gameboard that mark cells players
    suspect are bombs.
    @param gameboard the gameboard on which flags will be placed
    @param orig_val_dict a dictionary that stores flag coords and their original contents (so they can be reverted PRN)
    @param x the column number of the cell to flag
    @param y the row number of the cell to flag
    """
    # Check if previously flagged
    if gameboard[y][x] != 'X' and gameboard[y][x] != 'x': # Unflagged
        orig_val_dict[(x,y)] = gameboard[y][x] # Store original value
#        print((x,y))
#        print(gameboard[y][x])
        gameboard[y][x] = 'X' if gameboard[y][x] == -1 else ('x') # marker for flagged cell
    else: # Is flagged, time to toggle
#        print(orig_val_dict[(x,y)])
        gameboard[y][x] = orig_val_dict[(x,y)]
        orig_val_dict.pop((x,y))


def game(width, height, n):
    """
    This function executes a game of mine sweeper with the given height, width,
    and number of mines.
    @param height the number of rows in the gameboard
    @param width the number of columns in the gameboard
    @param n the number of mines randomly placed on the gameboard
    """
    # Gboard creation
    print("Creating your gameboard...")
    gboard = create_board(width, height)
    # Dict for tracking flags!
    fc2origval = {}
    # Burying mines
    print("Burying mines...")
    bury_mines(gboard, n)
    
    mine_found = False
    start_time = time.time()
    # Looping for coords!
    while not mine_found and not check_won(gboard):
        # Display board
        print("This is the current state of the board!")
        user_view(gboard)
        # Displaying time spent trying to complete board
        elapsed_time = time.time() - start_time
        print("Time Elapsed: {} secs".format(int(elapsed_time)))
        
        # Taking in coords
        xy_str = input("Enter the coordinates of the cell you want to uncover, or 'm' before this set of coordinates to place a flag (Format: x,y): ")
        # FLAG MODE!!!
        if xy_str[0] == "m":
            xy_li = xy_str[1:].split(",")
            x = int(xy_li[0])
            y = int(xy_li[1])
            place_flag(gboard,fc2origval,x,y)
        # UNCOVERING MODE
        else: 
            xy_li = xy_str.split(",")
            x = int(xy_li[0])
            y = int(xy_li[1])
            
            # Check if bomb
            if gboard[y][x] == -1: # Bomb! Ya done lost!!!
                mine_found = True # end looping of game! GAME OVER!
                print("GAME OVER!!!")
                # Displaying time spent trying to complete board
                elapsed_time = time.time() - start_time
                print("Time Elapsed: {} secs".format(int(elapsed_time)))
                print_mines(gboard)
            else: # No bomb!
                uncover_board(gboard, x, y)
    if not mine_found: # Meaning that discovering all non-bombs was cause of loop end, WINNER
        print("YAY!!! YOU WIN!!!")
        # Displaying time spent trying to complete board
        elapsed_time = time.time() - start_time
        print("Time Elapsed: {} secs".format(int(elapsed_time)))
    

game(10,10,20)

"""
gboard = create_board(10,10)
print("New Blank Gameboard!")
pprint(gboard)

bury_mines(gboard, 6)
print("Buried some mines!")
pprint(gboard)

print("Printing mine locats!")
print_mines(gboard)

print("Printing mine locats and adjacency indicators!!")
print_board(gboard)

print("Showing user's view!")
user_view(gboard)
"""
