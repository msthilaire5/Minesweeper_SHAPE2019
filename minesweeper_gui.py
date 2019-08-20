#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 14:49:58 2019

@author: msthilaire
"""

import random
# For keeping track of time to solve board
import time
# For GUI!
from tkinter import Tk, Label, Button, Frame, Canvas
# Functions from text-based version
from minesweeper_text import create_board, bury_mines, get_mine_count, print_board, uncover_board, place_flag, check_won


def display_board(board, canvas):
    """
    This function carries out graphical display of gameboard.
    @param board: the board model to display
    @param canvas: the Canvas object (from TkInter) to put shapes on.
    """
    
    # Prevent slowing down so not just piling stuff on top of shtuff
    canvas.delete("all")
    
    widthpxl = len(board[0]) * 31
    heightpxl = len(board) * 31
    
    for canvas_y in range(0,heightpxl,31):
        row = canvas_y // 31
        for canvas_x in range(0,widthpxl,31):
            col = canvas_x // 31
            # Cell content
            cell_text = ''
            if board[row][col] == -1 or board[row][col] == None: # Undiscovered, maybe mine locat
                cell_color = 'grey'
            elif board[row][col] == 'X' or board[row][col] == 'x':
                cell_color = 'light blue'
                cell_text = chr(9873)
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
    # Dict for holding flagged cell values
    fc2origval = {}
    # Burying mines
    print("Burying mines...")
    bury_mines(gboard, 10)
    print_board(gboard)
    
    # Creating window
    root = Tk()
    root.wm_title("Minesweeper")
    # Prep for canvas widget
    heightpxl = (len(gboard) * 31)
    widthpxl = (len(gboard[0]) * 31)
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
            canvas.unbind("<Button-2>")
            canvas.unbind("<Button-3>")
            # Display loss screen
            canvas.create_rectangle(0, 0, widthpxl - 1, heightpxl - 1, fill="red")
            canvas.create_text(widthpxl // 2, heightpxl // 2, font="arial 20", text="YOU LOSE!!!")
        else:
            # Change gboard val
            uncover_board(gboard, x, y)
            # Update view
            display_board(gboard,canvas)
        # Check if won
        if check_won(gboard):
            print("YAY!!! YOU WON!!!")
            canvas.unbind("<Button-1>")
            canvas.unbind("<Button-2>")
            canvas.unbind("<Button-3>")
            # Display win screen
            canvas.create_rectangle(0, 0, widthpxl - 1, heightpxl - 1, fill="green")
            canvas.create_text(widthpxl // 2, heightpxl // 2, font="arial 20", text="YOU WIN!!!")
    def handle_click_right(event):
        # Pull coords of click and translate to row/col
        x = event.x // 31
        y = event.y // 31
        print("Coords: {}, {}".format(x,y))
        place_flag(gboard,fc2origval,x,y)
        display_board(gboard,canvas)
    
    # Binding event handler to canvas widget
    # Right-click is Button-2 on Mac!!!! But Button-3 on Windows!!!
    canvas.bind("<Button-1>", handle_click)
    canvas.bind("<Button-2>", handle_click_right)
    canvas.bind("<Button-3>", handle_click_right)
    # Display the window now!!
    root.mainloop()
    
run_gui()
print("Game closed.")