import json, datetime, random, math, time
#from colr import base, color
import curses
from string import Template
import itertools
import re

global pro_badge, backup_badge

global height, width

sweep, defen, dog = ("Progress Sweeper", "Progress Defender", "ProgressDOG")
neo, savr, xl, colr = ("Matrix", "3DSavr", "PBXL", "Color")
jig, tetris, cmd = ("Jigsaw Puzzle", "Knockoff Tetris", "Progress Commander")

baseline = ["Relax", "Normal", "Hardcore"]
default = baseline + [sweep, defen] #relax, normal, hardcore, sweeper, defender
bonus = default + [dog, neo, savr] #relax, normal, hardcore, sweep, def, pbstein, matrix, savr
probonus = bonus + [xl]

baselineBAR = ["Casual", "Regular", "High-End"]
bonusBAR = baselineBAR + [colr, jig]

flatten = lambda m: [item for sublist in m for item in sublist]

#the index of what each sys has
backup_badge = pro_badge = {
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

backup_badge = pro_badge

lev = ["Pro", "Expert", "Master", "Adept", "Grand"] #the badges
levcount = [100, 250, 500, 1000] #the amt you need for each (excluding pro)


class save:
    def __init__(self, filen, new=False):
       self.index = {
            "hw": ["PB95", "PB95+", "PB98", "MEME", "PB2000", "XB", "Wista", "7", "81", "10", "1X", "11"],
            "beta": ["Largehorn", "Whisper", "Chitown"],
            "pro": ["PB 3.14", "PB2", "PB1", "PB-DOS"],
            "exp": ["PB NOT 4.0", "PB NOT 3.60"],
            "bar": ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10", "B10.2", "B10.3", "B11"],
        }
       
       self.file = filen
       try:
           with open(filen, "r") as f:
               self.data = json.load(f)
       except Exception as e:
            if not new: raise(e)
            self.data = {"lock": [1]}

       try:
           self.list = self.generate(*self.data["lock"])
       except:
           self.list = self.generate(1)
       self.filter = lambda m: {x:y for x, y in m.items() if x in self.list}

    def generate(self, *inputs):
        retr = []
        for un, (_, os) in zip(inputs, self.index.items()):
                try:
                    retr.extend(os[:un])
                except:
                    pass
        self.list = retr
        return retr


cursav = save("pb95.json")
sav = [cursav]
sav.append("atext")

#pro_badge = cursav.filter(pro_badge)

"""
print(cursav.list)
print(cursav.generate(3, 3, 1, 2, 7))
print(cursav.list)
input()
"""

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


def rndo(curr="", out=False):
    gamem = None
    #curr = "PB NOT 4.0" #testing str
    output = [""]
    diff = 0
    try:
        if out == True and random.randint(0, 2) == 0: raise KeyError("lol ignore this")
        else:
            x = pro_badge[curr][1]
            gamem = random.choice(pro_badge[curr][1])
            os = [curr, gamem]
            output[0] = f"{curr} - {gamem}"
    except KeyError:
        os, gamem = random.choice(list(pro_badge.items()))
        gamem = random.choice(gamem[1])
        #os[1] = gamem
        output[0] = f"{os} - {gamem}"
        os = [os, gamem]
        diff = 1


    if gamem == "Custom":
        output[0] += "\n"
        jus = 20

        d_rand = ""
        ent = ("Pace", "Segment Speed", "Segment Wobble", "Wobble Speed", "Red Freq.", "Popup Freq.")
        l = len(max(ent, key=len))
        for x, y in enumerate(ent):
            rn = random.uniform(0, 0.4) if x == 4 else random.random()
            d = f"{y.ljust(l)}: {round(rn, 2)}   "
            #if x % 2: d += "\n"
            d += "\n"
            output[0] += d
        
        """output[0] += (f"Pace: {str(round(random.random(), 2)).ljust(jus)}Segments Speed: {round(random.random(), 2)}\n"
        f"Segment Wobble: {str(round(random.random(), 2)).ljust(jus)}Wobble Speed: {round(random.random(), 2)}\n"
        f"Freq. of Red: {str(round(random.randrange(0, 0.4), 2)).ljust(jus)}Freq. of popups: {round(random.random(), 2)}\n")"""
    
        output[0] += "\n"
        if random.randint(0, 1): output[0] += "Popups\t"
        if random.randint(0, 1): output[0] += "Level Puzzle\t"
        if random.randint(0, 1): output[0] += "Utilities"
        #output[0] += "\n"
    else:
        std = ["100% Blue", "95% Blue", "100% Yellow", "95% Yellow", "Two Stripes", "Yellow Caps", "Blue Caps", "50/50%", "5B 1O 4B 4O 1B 5O", "Alternating 1X", "Alternating 2X", "Alternating 3X", "Alternating 4X", "Blue 40%, Alternating"]
        std = (std, (*baseline, *baselineBAR, dog, neo, savr, xl, jig, cmd)) #the first part is the entries second is the gamemodes it applies to
        pinkb = (["Minus Bar"], (*baseline, *baselineBAR, neo, savr))
        nullb = (["NULL0"], (*baseline, *baselineBAR, neo, savr))
        

        gamespec = flatten([x for x, y in (std, pinkb, nullb) if (gamem in y)])
        try:
            gmod = random.choice(gamespec)
        except IndexError:
            gmod = None

        if random.randint(0, 2) != 0 and gmod != None:
            output[0] += f" ({gmod})"

    os.append(diff)
    output.extend(os)
    return output



def progress(count, total, bar_len, focus = False):

    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)

    return ('=' * filled_len + '-' * (bar_len - filled_len), filled_len)

def gennum(pro, score):
    retr = f"{str(score).rjust(4)} / {pro}"

    for n, labl, next in zip([pro, *levcount], lev, levcount):
        if score >= n: retr = f"{str(score).rjust(4)} / {next} ({labl})"
        else: break
    else:
        retr = f"{str(score).rjust(4)} (Grand)"
    return retr


def printbar(data, focus=None, coun = 0):

    cur = 0
    total = 0

    l = len(max(pro_badge.keys(), key=len))
    fstr = Template('${lb}$pb {${bar}} $cnt $newlbl')
    newlbl = "<-- NEW"
    barlen = int(width/2) - (l + len(fstr.substitute(lb="", pb=""*l, bar="9999/9999", cnt="", newlbl=""))) - 20
    
    for n, (pb, (pro, game)) in enumerate(pro_badge.items()):

        try:
            score = data[pb]
        except KeyError:
            score = 0

        cnt = gennum(pro, score)

        i = max(data.values())
        for x in [70, *levcount]:
            if i <= x-1:
                barmax = x + 1
                break
        else: barmax = i + 1 #getting the furthest num bar display

        n = f"{n + 1} "
        bar, count = progress(score, barmax, barlen)

        bar = list(bar) #converts it to a list to make it editable
        for x, y in zip(lev, [pro, *levcount]): #gets the list of badges
            try:
                ind = int(math.floor(barlen * y / float(barmax)))
                try: nextv = bar[ind + 1]
                except KeyError: nextv = "-"
                if bar[ind] == "=" and nextv == "-": x = x.lower()
                bar[ind] = x[0]  #sets the corresponding part in str to the first letter of badge
            except IndexError: pass #pass if its not shown in the bar
        bar = "".join(bar) #converts it back into a string

        cur += score
        total += barmax - 1

        yield (fstr.substitute(lb=n.rjust(3), pb=pb.rjust(l, "-"), bar=bar, cnt=cnt.ljust(20), newlbl=newlbl if focus == pb else ""), pb)

    bar, *_ = progress(cur, total, barlen)
    
    #n = f"\n{str(int(n) + 1)}"
    pb = "total"
    per = str(round(cur / total, 2))
    addin = f" ( +{round(coun / total, 6)}%)" if coun > 0 else ""
    yield (fstr.substitute(lb="\n", pb=pb.rjust(l+3), bar=bar, cnt=f"{str(cur).rjust(4)} / {total}", newlbl=f"\n\n{per.rjust(l+3)}%{addin}"), pb)


def numjump(screen, st):
    jump = st
    screen.addstr(height - 1, width - 2, st)
    c = chr(screen.getch())
    if not c.isnumeric(): return

    jump = int(f"{jump}{c}")

    try:
        ret = list(pro_badge.keys())[jump - 1]
        screen.addstr(0, 0, ret)
        return ret
        #curses.napms(2000)
    except:
        return






@curses.wrapper
def main(screen):
    global height, width, pro_badge
    screen.clear()
    screen.refresh()

    height, width = screen.getmaxyx()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE) #filled bar
    curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK) #unfocused bar
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_GREEN) #the bar foc
    curses.init_pair(7, curses.COLOR_GREEN, curses.COLOR_BLACK) #curos in the leaderboards
    l = len(max(pro_badge.keys(), key=len))

    print_center("Press any key to start or q to close", screen, curses.COLOR_BLUE)

    try:
        with open("pb95.json", "r") as f:
            data = org = json.load(f)
        for x in pro_badge.keys():
            if x not in data.keys():
                data[x] = 0
    except Exception as e:
        data = {x: 0 for x in pro_badge.keys()}



    

    dif = 0
    num = 0
    count = 0
    pb = ""
    sort = 0

    while True:

        c = chr(screen.getch())
        if c == "q": break

        if c == " ":
            try:
                data[pb] += 1
                count += 1
            except KeyError:
                pass
        if c == "-":
            try:
                data[pb] -= 1
                count -= 1
            except KeyError:
                pass
        if c == "r":
            pb = ""

        if c == "m":
            if sort == 1:
                pro_badge = backup_badge
                sort = 0
                pb = ""
            else:
                sort = 1

        if sort == 1:
            dif = {}
            for n, (pb, (pro, *_)) in enumerate(pro_badge.items()):
                try:
                    s_data = data[pb]
                except KeyError: s_data = 0
                for y in (pro, *levcount):
                    dif[pb] = y - s_data
                    if dif[pb] > 0: break

            pro_badge = dict(sorted(pro_badge.items(), key= lambda m: dif[m[0]]))
            pb = list(pro_badge.keys())[0]
            num = 0
    

        elif c.isnumeric():
            tmp = numjump(screen, c)
            if tmp:
                pb = tmp
                x = 0
            else: continue

        screen.addstr(0, 0, c)

        with open("pb95.json", "w") as f:
                json.dump(data, f, indent=4)


        screen.clear()
        screen.refresh()

        barwidth = int(width / 2)
        barwin = curses.newpad(500, barwidth + 10)
        screen.move(0, 0)

        d_game, pb, *_, dif = rndo(pb, True if num >= 3 else False)
        if dif:
            num = 0
        else: num += 1
        
        for n, (x, cur) in enumerate(printbar(data, pb, count), 1):
            for y in list(filter(lambda x:x!=None and not x.isspace() and x!="", re.split(r"((?:P|p)?=+\w*(?:=|[a-z]))|(=)|(p|P)", x))):
                
                if re.match(r"(=+(?:\w*=+|=|[a-z]))", y):
                    if pb == cur: barwin.addstr(str(y), curses.color_pair(6))
                    else: barwin.addstr(str(y), curses.color_pair(1))
                #elif re.match(r"^-+$", y):
                #    barwin.addstr(str(y), curses.color_pair(2))
                else:
                    barwin.addstr(str(y))
            barwin.addstr("\n")

        for n, x in enumerate(d_game.splitlines()):
            screen.addstr(n+2, width-40, x)

        barwin.refresh(0, 0, 0, 0, height - 1, width - 1)

        topwin = curses.newpad(9900, barwidth)
        topwin.addstr("Top Levels\n")



        sp = 0
        for x, y in zip((pro_badge[pb][0], *levcount), lev):
            if data[pb] >= x: continue
            sp = (x, y)
            break


            
        tmp = dict(sorted(data.items(), key=lambda m: data[m[0]], reverse=True))
        #tmp = {x: y for x, y in data.items() if x in pro_badge.keys()}
        try:
            del tmp["achivements"]
        except: pass

        if True:
            iterate = itertools.zip_longest(tmp.items(), (curses.color_pair(3), curses.color_pair(4), curses.color_pair(5)), fillvalue=0) #making it iterable
            y = list(tmp.keys())
            try:
                pbindex = list(tmp.keys()).index(pb)
                for x in range(10):
                    key = y[pbindex - x]
                    val = tmp[key]
                    if val != tmp[pb]: break

                    topent = 1 if list(tmp.values())[0] == tmp[pb] else 0
            except:
                key = y[-1]
                val = 0
            
            
            u = 0
            for (x, y), c in iterate:
                if pb == x and not c:
                    c = curses.color_pair(7)
                if key == x:
                    u = 1
                    d_next = f"(Only {val - tmp[pb]} levels to go!)" if topent != 1 else ""
                else: d_next = ""

                if x in lev:
                    topwin.addstr(f"(Only {y - data[pb]} levels to {x})\n", curses.color_pair(2))
                    continue

                #
                #print(color(f"{x.rjust(l)} - {y} {d_next}", fore=c))
                if y < sp[0]:
                    topwin.addstr(f"Only {sp[0] - data[pb]} levels to {sp[1]}\n", curses.color_pair(2))
                    sp = (0, 0)
                topwin.addstr(f"{x.rjust(l)} - {y} {d_next}\n", c)
                #if pb.startswith("PB NOT") and n == 1: break
            else:
                try:
                    #if u == 0 and topent != 1 : topwin.addstr(f"{key.rjust(l)} - {val} (Only {val - tmp[pb]} levels to go!)\n")
                    pass
                except: pass
        topwin.refresh(0, 0, 1, barwidth+10, height-1, width-1)
        screen.addstr(height - 1, 0, "Press ? for help (not implemented)")
        if c == "?":
            screen.addstr(height - 1, 0, "Havn't implemented this yet, don't forget future me :)")
        screen.refresh()
