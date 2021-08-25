import json, datetime, random, math, time
from colr import base, color
import curses



def reload_score():
    with open("pb95.json", "r") as f:
    #json.dump(arr, file, indent=4)
        return json.loads(f.read())

# Make a function to print a line in the center of screen
def print_center(message, screen, *kwargs):
    num_rows, num_cols = screen.getmaxyx()

    # Calculate center row
    middle_row = int(num_rows / 2)

    # Calculate center column, and then adjust starting position based
    # on the length of the message
    half_length_of_message = int(len(message) / 2)
    middle_column = int(num_cols / 2)
    x_position = middle_column - half_length_of_message

    # Draw the text
    screen.addstr(middle_row, x_position, message, *kwargs)
    screen.refresh()

def printbar(focus = None):
    sweep, defen, dog = ("Progress Sweeper", "Progress Defender", "ProgressDOG")
    neo, savr, xl, colr = ("Matrix", "3DSavr", "PBXL", "Color")
    jig, tetris, cmd = ("Jigsaw Puzzle", "Knockoff Tetris", "Progress Commander")

    baseline = ["Relax", "Normal", "Hardcore"]
    default = baseline + [sweep, defen] #relax, normal, hardcore, sweeper, defender
    bonus = default + [dog, neo, savr] #relax, normal, hardcore, sweep, def, pbstein, matrix, savr
    probonus = bonus + [xl]

    baselineBAR = ["Casual", "Regular", "High-End"]
    bonusBAR = baselineBAR + [colr, jig]


    #the index of what each sys has
    pro_badge = {
        "PB-DOS": [10, baseline + [tetris, cmd]],
        "PB1": [10, default],
        "PB2": [10, default],
        "PB 3.14": [10, bonus],
        "PB NOT 3.60": [10, ["Custom"]],
        "Chitown": [10, ["Normal"]], #lets pray these are accurate
        "PB95": [10, [x for x in bonus + [cmd] if x not in ("Relax", "Hardcore", defen)]], #indir
        "PB95+": [20, [x for x in probonus + [cmd] if x not in ("Hardcore")]], #indir
        "PB NOT 4.0": [30, ["Custom"]], #confirmed
        "PB98": [20, probonus + [cmd]], #indir
        "MEME": [30, probonus], #indir
        "PB2000": [30, probonus], #indir
        "Whisper": [30, bonus], #indir
        "XB": [30, probonus], #indir
        "Largehorn": [60, bonus], #confirmed, (funny enough this one varies)
        "Wista": [40, probonus], #indir
        "7": [40, probonus], #indir
        "81": [50, probonus], # (frick i already got expert)
        "10": [50, default + [dog]], #confirmed also what??
        "1X": [60, probonus],
        "11": [60, default + [dog]],

        #barOS
        "B1": [10, ["Regular"]],
        "B2": [20, ["Casual", "Regular"]],
        "B3": [30, baselineBAR],
        "B4": [40, baselineBAR], #confirmed
        "B5": [50, baselineBAR], #confirmed
        "B6": [60, baselineBAR], #confirmed
        "B7": [60, bonusBAR], #semi confirmed
        "B8": [70, bonusBAR], #confirmed
        "B9": [70, bonusBAR], #confirmed
        "B10": [70, bonusBAR], #confirmed
        "B10.2": [70, bonusBAR], #confirmed
        "B10.3": [70, bonusBAR], #confirmed
        "B11": [70, bonusBAR]

        #"achivements": 86

        #60
    }

    for pb, (pro, game) in pro_badge.items():
        yield pb




@curses.wrapper
def main(screen):
    screen.clear()
    screen.refresh()

    height, width = screen.getmaxyx()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE) #filled bar
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK) #unfocused bar

    print_center("Press any key to start or q to close", screen, curses.COLOR_BLUE)

    while (c := chr(screen.getch())) != "q":
        screen.clear()
        screen.refresh()

        win = [x for x in printbar()]
        barwidth = int(width / 2)
        barwin = curses.newpad(100, barwidth)
        for n, x in enumerate(win):
            barwin.addstr(n, 0, str(x))
        
        barwin.refresh(0, 0, 0, 0, height - 1, width - 1)
