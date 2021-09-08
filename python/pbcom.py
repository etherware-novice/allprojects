import curses, random
from curses.textpad import rectangle

global row, col, curbar

def comwindow(screen):

    row, col = screen.getmaxyx()
    spawn_ul = (4, int(col/2) - 20)
    spawn_lr = (25, int(col/2) - 2)
    rectangle(screen, *spawn_ul, *spawn_lr)


    bar_ul = (4, int(col/2) + 2)
    bar_lr = (25, int(col/2) + 20)
    rectangle(screen, *bar_ul, *bar_lr)

    return ((*spawn_ul, *spawn_lr), (*bar_ul, *bar_lr))


@curses.wrapper
def main(screen):

    global curbar

    curses.raw(True)
    curses.cbreak(True)
    curses.noqiflush()
    curses.curs_set(0)
    screen.nodelay(1)

    row, col = screen.getmaxyx()
    spw_cord, bar_cord = comwindow(screen)

    seg = ["Blue", "Blue x2", "Blue x3", "Yellow", "Pink", "RED", "Green"]
    weight = [50, 20, 10, 50, 30, 35, 5]

    screen.refresh()

    curseg = "Blue"
    cury = spw_cord[0] - 1
    timedely = 0
    curbar = []
    while True: #ascii for q
        c = screen.getch()
        if c == 113: break

        if c in (68, 100, 261):
            if curseg == "RED":
                screen.clear()
                screen.addstr("dainsdoadnqwed9012eje129d09/d012e@(EU@!$(_U")
                screen.addstr(row - 1, 0, "GAME OVER")
                screen.refresh()
                curses.napms(5000)
                return

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

                if curseg == "Green":
                    curbar = ["Blue"] * 20

            else:
                screen.addstr(cury, spw_cord[1] + 1, "000".center(17))

            curseg = ""
            if len(curbar) >= 20: return

        if c == 97: #lowercase a
            curseg = ""
            curbar = ["Blue"] * 19

        if c == 98:
            curseg = ""

        for n, x in enumerate(curbar):
            screen.addstr(bar_cord[2] - n - 1, bar_cord[1] + 1, f"{x}_{20-n}".center(17))

        if timedely != 4000 * 2: 
        #if timedely != 50000:
            timedely += 1
            continue
        else: timedely = 0
        
        screen.erase()
        comwindow(screen)
        if curseg == "": 
            curseg, *_ = random.choices(seg, weights=weight, k=2)
            cury = spw_cord[0] - 1

        cury += 1

        tmp = cury - spw_cord[0]
        #screen.addstr(0, 0, str(21 - tmp))
        #screen.addstr(1, 0, str(tmp))
        #screen.addstr(2, 0, str(len(curbar)))

        if cury >= spw_cord[2]:
            curseg = ""
            continue
        screen.addstr(cury, spw_cord[1] + 1, curseg.center(16))

        #261 - right arrow
        #100 - lowercase w
        #68 - uppercase W




        screen.refresh()

        #curses.napms(1000)



if len(curbar) >= 20: print("YOU WIN")
else: print("Better luck next time...")

print()
for x in ("Blue", "Yellow"):
    print(f"{x.rjust(10)} - {curbar.count(x) * 5}%")

pbbar = [1 if x == "Blue" else 0 for x in curbar]

if pbbar.count(1) >= 20: print("Perfectionst Bonus\n")
if pbbar.count(0) >= 20: print("Noncomformist Bonus\n")
if pbbar == [1 for i in range(19)] + [0]: print("95% Bonus\n")
if pbbar == [0 for i in range(19)] + [1]: print("Noncomformist 95% Bonus\n")
if pbbar.count(1) == pbbar.count(0): print("50/50 Bonus\n")

pattern = [1, 0] * 10
altpattern = [0, 1] * 10

if pbbar == pattern or pbbar == altpattern: print("Pattern Bonus\n")
if pbbar == [1, 1, 0, 0] * 5 or pbbar == [0, 0, 1, 1] * 5: print("Pattern x2 Bonus\n")
if pbbar == [1, 1, 1, 0, 0, 0] * 3 + [1, 1] or pbbar == [0, 0, 0, 1, 1, 1] * 3 + [0, 0]: print("Pattern x3 Bonus\n")
if pbbar == [1, 1, 1, 1, 0, 0 ,0 ,0] * 2 + [1, 1, 1, 1] or pbbar == [0, 0, 0, 0, 1, 1, 1, 1] *2 + [0, 0, 0, 0]: print("Pattern x4 Bonus\n")
if pbbar == [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0 ,0 ,0 ,0 ,0]: print("95 in morse code..Bonus\n")


try:
    if pbbar[:9] == pbbar[10:].reverse(): print("Symmetry Bonus\n")
except: pass

print(pbbar)

print()



    

    #curses.napms(2000)
