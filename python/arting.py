import json, datetime, random, math, time
from colr import base, color
import curses

global data

file = "arting.json"
fillclr = lambda m, n: color(m[:n], back=(28, 108, 158)) + m[n:]
fillmulti = lambda m, n, o: color(m[:n], back=(28, 108, 158)) + color(m[n:o], back=(21, 176, 34)) + m[o:]
filllast = lambda m, n: color(m[:n-1], back=(28, 108, 158)) + color(m[n], back=(21, 176, 34)) + m[n:]
round_down = lambda num, divisor=5: num - (num%divisor)



indbar = lambda m, n: int(math.floor(barlen * m / float(n))) #gets an index of the bar
barlen = 20


with open(file, "r") as f:
    #json.dump(arr, file, indent=4)
    bkup = data = json.loads(f.read())


roundup = lambda x: int(math.ceil(x / 10.0)) * 10


def updsub():
    try:
        now = datetime.datetime.now()
        t = data["ltime"]
        if t.date() + datetime.timedelta(weeks=1) <= now.date():
            l = random.choice(data.keys())
            t = now
        else:
            l = data["lsub"]
    except KeyError:
        l = datetime.datetime.now()
        t = random.choice(data.keys())
        
    return (t, l)

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


def progress(count, total, bar_len, focus = False):

    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)

    return ('=' * filled_len + '-' * (bar_len - filled_len), filled_len)

#ltime, lsub = updsub()

def printbar():
    global data

    l = len(max(data.keys(), key=len))

    t = random.choice(list(data.keys()))
    data = {m:n+6 for m, n in data.items()}
    m = max(data.values())
    barmax = roundup(m + 1)
    del m
    
    for x, y in data.items():

        old = bkup[x]        

        bar, count = progress(y, barmax, barlen)
        d_num = f" {y} / {barmax}"
        #bar = (bar, count)

        #if y > old:
        if False:
            oldind = indbar(old, barlen)
            if oldind >= count: bar = filllast(bar, count)
            else: bar = fillmulti(bar, oldind, count)
            d_num += f" (+{y - old})"
        #else:
        #    bar = fillclr(bar, count)


        display = f"{x.rjust(l)} {{{bar}}} {d_num}"

        yield (x.rjust(l), bar, d_num, count)




@curses.wrapper
def main(screen):
    screen.nodelay(True)
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_WHITE ,curses.COLOR_BLUE)
    while False:
        now = datetime.datetime.now()
        secdown = round_down(now.second)
        now = now.replace(second=secdown)
        print_center(now.strftime("%A, %B %d, %H:%M:%S"), screen)
        screen.refresh()
        time.sleep(0.5)

        if (c := screen.getch()) in (3, 26): raise KeyboardInterrupt

    for n, bar, r, i in printbar():
        screen.addstr(f"{n} {{ ")
        screen.addstr(bar[:i], curses.color_pair(1))
        screen.addstr(f"{bar[i:]} }}")
        screen.addstr(f"{r}\n")

    screen.refresh()
    curses.napms(100000000)