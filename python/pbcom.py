import curses, random
from curses.textpad import rectangle

global row, col

def comwindow(screen):

    row, col = screen.getmaxyx()
    spawn_ul = (4, int(col/2) - 20)
    spawn_lr = (row - 5, int(col/2) - 2)
    rectangle(screen, *spawn_ul, *spawn_lr)


    bar_ul = (4, int(col/2) + 2)
    bar_lr = (row - 5, int(col/2) + 20)
    rectangle(screen, *bar_ul, *bar_lr)

    return ((*spawn_ul, *spawn_lr), (*bar_ul, *bar_lr))


@curses.wrapper
def main(screen):

    curses.raw(True)
    curses.cbreak(True)
    curses.noqiflush()
    curses.curs_set(0)
    screen.nodelay(1)

    row, col = screen.getmaxyx()
    spw_cord, bar_cord = comwindow(screen)

    seg = ["Blue", "Blue x2", "Blue x3", "Yellow", "Pink", "RED"]
    weight = [10, 5, 2, 10, 7, 5]

    screen.refresh()

    curseg = "Blue"
    cury = spw_cord[0] - 1
    timedely = 0
    curbar = []
    while (c := screen.getch()) != 113: #ascii for q

        if c in (68, 100, 261):
            if curseg == "RED":
                screen.clear()
                screen.addstr("dainsdoadnqwed9012eje129d09/d012e@(EU@!$(_U")
                screen.addstr(row - 1, 0, "GAME OVER")
                screen.refresh()
                curses.napms(5000)
                exit()

            tmp = cury - spw_cord[0] #look idk why it forces me to do this
            if 21 - tmp >= len(curbar): #if the piece doesnt "crash"
                if "Blue" in curseg:
                    curbar.append("Blue")
                if curseg == "Blue x2" or curseg == "Blue x3":
                    curbar.append("Blue")
                if curseg == "Blue x3":
                    curbar.append("Blue")
                
                if curseg == "Yellow":
                    curbar.append("Yellow")

                if curseg == "Pink":
                    n = len(curbar)
                    try:
                        curbar.pop()
                    except: pass
                    screen.addstr(bar_cord[2] - n, bar_cord[1] + 1, f"Minus".center(17))

                    screen.refresh()
                    curses.napms(500)

            else:
                screen.addstr(cury, spw_cord[1] + 1, "000".center(17))

            curseg = ""

        if c == 97: #lowercase a
            curseg = ""

        for n, x in enumerate(curbar):
            screen.addstr(bar_cord[2] - n - 1, bar_cord[1] + 1, f"{x}_{20-n}".center(17))

        if timedely != 4000 * 2: 
            timedely += 1
            continue
        else: timedely = 0
        
        screen.clear()
        comwindow(screen)
        if curseg == "": 
            curseg, *_ = random.choices(seg, weights=weight)
            cury = spw_cord[0] - 1

        cury += 1

        tmp = cury - spw_cord[0]
        screen.addstr(0, 0, str(21 - tmp))
        screen.addstr(1, 0, str(tmp))
        screen.addstr(2, 0, str(len(curbar)))

        if cury >= spw_cord[2]:
            curseg = ""
            continue
        screen.addstr(cury, spw_cord[1] + 1, curseg.center(16))

        #261 - right arrow
        #100 - lowercase w
        #68 - uppercase W




        screen.refresh()

        #curses.napms(1000)







    

    #curses.napms(2000)
