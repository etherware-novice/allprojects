import curses
from curses.textpad import Textbox, rectangle
import subprocess, os

# Make a function to print a line in the center of screen
def print_center(message, screen):
    num_rows, num_cols = screen.getmaxyx()

    # Calculate center row
    middle_row = int(num_rows / 2)

    # Calculate center column, and then adjust starting position based
    # on the length of the message
    half_length_of_message = int(len(message) / 2)
    middle_column = int(num_cols / 2)
    x_position = middle_column - half_length_of_message

    # Draw the text
    screen.addstr(middle_row, x_position, message)
    screen.refresh()



@curses.wrapper
def main(screen):
    screen.addstr(0, 0, "Enter IM message: (hit Ctrl-G to send)")

    editwin = curses.newwin(5,30, 2,1)
    rectangle(screen, 1,0, 1+5+1, 1+30+1)
    screen.refresh()

    box = Textbox(screen)

    # Let the user edit until Ctrl-G is struck.
    box.edit()

    # Get resulting contents
    message = box.gather()

    curses.napms(3000)
    print(message)