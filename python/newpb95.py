import yaml
import math
from colr import color
import os
import random
import itertools, getopt, sys

#all the baseline vars that are used throughout this

global data

barbg = (28, 108, 158) #the bg color of the colored in part
#barbg = (110, 56, 235)
barlen = 100 #how long the bar is
barmax = -1 #251 #the furthest value the bar will disp (note if its equal to a badge it wont show up)
#setting it to -1 sets it to automatic mode

#gamemode vars def
baseline = ["Relax", "Normal", "Hardcore"]
default = baseline + ["Progress Sweeper", "Progress Defender"] #relax, normal, hardcore, sweeper, defender
bonus = default + ["ProgressDOG", "Matrix", "3DSavr"] #relax, normal, hardcore, sweep, def, pbstein, matrix, savr
probonus = bonus + ["PBXL"]

baselineBAR = ["Casual", "Regular", "High-End"]
bonusBAR = baselineBAR + ["Color", "Jigsaw Puzzle"]

#small util functs
indbar = lambda m, n: int(math.floor(barlen * m / float(n))) #gets an index of the bar
aplcolr = lambda m, n, o=barbg, **p: color(m[:n], back=o, **p) + m[n:] #colors in part of the str
aplall = lambda m, n, o=barbg, p=None: color(m[:n], back=o) + color(m[n:], fore=p)



#the index of what each sys has
global pro_badge
pro_badge = {
    "PB-DOS": [10, ["Relax", "Normal", "Hardcore", "Knockoff Tetris", "Progress Commander"]],
    "PB1": [10, default],
    "PB2": [10, default],
    "PB 3.14": [10, bonus],
    "PB NOT 3.60": [10, ["Custom"]],
    "Chitown": [10, ["Normal"]], #lets pray these are accurate
    "PB95": [10, [x for x in bonus + ["Progress Commander"] if x not in ("Relax", "Hardcore", "Progress Defender")]], #indir
    "PB95+": [20, [x for x in probonus + ["Progress Commander"] if x not in ("Hardcore")]], #indir
    "PB NOT 4.0": [30, ["Custom"]], #confirmed
    "PB98": [20, probonus + ["Progress Commander"]], #indir
    "MEME": [30, probonus], #indir
    "PB2000": [30, probonus], #indir
    "Whisper": [30, bonus], #indir
    "XB": [30, probonus], #indir
    "Largehorn": [60, bonus], #confirmed, (funny enough this one varies)
    "Wista": [40, probonus], #indir
    "7": [40, probonus], #indir
    "81": [50, probonus], # (frick i already got expert)
    "10": [50, default + ["ProgressDOG"]], #confirmed also what??
    "1X": [60, default + ["ProgressDOG"]],
    "11": [60, default + ["ProgressDOG"]],

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

def load_usr():
    try:
        with open(r'pb95.yaml') as file:
            #raise(IOError)
            return yaml.load(file, Loader=yaml.FullLoader) #loads the users score
    except (IOError, OSError) as e:
        return {x: 0 for x in pro_badge.keys()}


lev = ["Pro", "Expert", "Master", "Adept", "Grand"] #the badges
levcount = [100, 250, 500, 1000] #the amt you need for each (excluding pro)

tmp, _ = getopt.getopt(sys.argv[1:], "opn")
if any("-o" in sl for sl in tmp): dump_ = 1
elif any("-p" in sl for sl in tmp): dump_ = 2
elif any("-n" in sl for sl in tmp): dump_ = 3
else: dump_ = False

def sort():
    dif = {}
    data = load_usr()
    if dump_ == 1: return dict(sorted(pro_badge.items(), key=lambda m: data[m[0]], reverse=True))
    elif dump_ == 2: return dict(sorted(pro_badge.items(), key=lambda m: pro_badge[m[0]][0]))
    elif dump_ == 3: 
        for n, (pb, (pro, *_)) in enumerate(pro_badge.items()):
            try:
                s_data = data[pb]
            except KeyError: s_data = 0
            for y in (pro, *levcount):
                dif[pb] = y - s_data
                if dif[pb] > 0: break
        return dict(sorted(pro_badge.items(), key= lambda m: dif[m[0]]))
            #exit()
    else: return pro_badge

#defining the bar thats used
def progress(count, total, bar_len, focus = False):

    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)

    return ('=' * filled_len + '-' * (bar_len - filled_len), filled_len)

#the numerical representation of the score on the right part
def gennum(pro, score):
    retr = f"{str(score).rjust(4)} / {pro}"

    for n, labl, next in zip([pro, *levcount], lev, levcount):
        if score >= n: retr = f"{str(score).rjust(4)} / {next} ({labl})"
        else: break
    else:
        retr = f"{str(score).rjust(4)} (Grand)"
    return retr


#main
def genbar(focus = None):
    global barmax, data
    global totamt
    global tot
    global pro_badge
    global l
    totamt = 0
    tot = 0

    xy = 0 #index

    data = load_usr()
    if dump_ > 0 and dump_ != 3: focus = None


        #data = {"B1": 0, "achivements": 1}

    if barmax == -1:
        i = max(data.values())
        for x in [70, *levcount]:
            if i <= x-1:
                barmax = x + 1
                break
        else: barmax = 1001
    
    for pb, (pro, game) in pro_badge.items(): #loads frin the index of what each game has
        xy += 1 #inc
        try:
            score = data[pb] #loads the score from the data file earlier
        except KeyError:
            score = 0 #defaults to 0

        for x, y in zip(lev, (pro, *levcount)):
            dif_amt = y - score
            dif_lbl = x
            if dif_amt > 0: break


        bar, count = progress(score, barmax, barlen) #gets the actual bar used

        bar = list(bar) #converts it to a list to make it editable
        for x, y in zip(lev, [pro, *levcount]): #gets the list of badges
            try:
                bar[indbar(y, barmax)] = x[0] #sets the corresponding part in str to the first letter of badge
            except IndexError: pass #pass if its not shown in the bar
        bar = "".join(bar) #converts it back into a string

        d_amt = gennum(pro, score) #calls the function to get the display val

        l = len(max(pro_badge.keys(), key=len)) #gets the longest value in the list of systems for formatting
        if pb == "B1" and not dump_: 
            print('\n')
            print('BarOS:'.rjust(l + 1)) #seperator
        ffs = "-"
        sysp = pb.rjust(l, ffs) #formats the system display name to be to the right with -'s in it

        if count > 0: 
            if pb == focus: bar = aplcolr(bar, count, (56, 235, 77), fore=(23, 23, 27))
            else: 
                bar = aplall(bar, count, p=(50,50,50)) #colors in the bar
        elif pb != focus: bar = color(bar, fore=(50, 50, 50))
        nw = color("<------ NEW", fore=(37, 219, 65)) if pb == focus else ""
        d_if = f"  (Only {dif_amt} to {dif_lbl})" if dump_ == 3 else ""

        #if sys != "B1" and sys == focus: print("")
        #if sys == focus: print("\n")
        print(f"{str(xy).rjust(2)}-{sysp} [{bar}]{d_amt.ljust(20)}{d_if.ljust(20)} {nw}") #displays evreything
        #if sys != "1X" and sys != "B10.3" and sys == focus: print("")
        #if sys == focus: print("\n")

        tot += 1000
        totamt += score
    
    print("\n")
    try:
        score = data["achivements"]
    except:
        score = 0
    sysp = "achivements".rjust(l + 3)
    bar, count = progress(score, 89, barlen)
    if count > 0: bar = aplcolr(bar, count)
    print(f"{sysp} [{bar}]  {str(score).rjust(2)} / 89")

    sysp = "total".rjust(l + 3)
    bar, count = progress(totamt, tot, barlen)
    if count > 0: bar = aplcolr(bar, count)
    print(f"{sysp} [{bar}]  %{round(100.0 * totamt / float(tot), 4)}")
    
    print(f"levels: {totamt}")



##random choice sect
def call(curr:str = "", out = False):
    gamem = None
    output = [""]
    try:
        if out == True and random.randint(0, 2) == 0: raise KeyError("lol ignore this")
        else:
            if dump_: curr = list(pro_badge.keys())[0]
            x = pro_badge[curr][1]
            gamem = random.choice(pro_badge[curr][1])
            os = [curr, gamem]
            output[0] = f"{curr} - {gamem}"
    except KeyError:
        os, gamem = random.choice(list(pro_badge.items()))
        if dump_:
            os = list(pro_badge.keys())[0]
            gamem = random.choice(pro_badge[os][1])


        else: gamem = random.choice(gamem[1])
        #os[1] = gamem
        output[0] = f"{os} - {gamem}"
        os = [os, gamem]


    if gamem == "Custom":
        output[0] += "\n"
        jus = 20

        d_rand = ""
        ent = ("Pace", "Segment Speed", "Segment Wobble", "Wobble Speed", "Red Freq.", "Popup Freq.")
        l = len(max(ent, key=len))
        for x, y in enumerate(ent):
            rn = random.uniform(0, 0.4) if x == 4 else random.random()
            d = f"{y.ljust(l)}: {round(rn, 2)}   "
            if x % 2: d += "\n"
            output[0] += d
        
        """output[0] += (f"Pace: {str(round(random.random(), 2)).ljust(jus)}Segments Speed: {round(random.random(), 2)}\n"
        f"Segment Wobble: {str(round(random.random(), 2)).ljust(jus)}Wobble Speed: {round(random.random(), 2)}\n"
        f"Freq. of Red: {str(round(random.randrange(0, 0.4), 2)).ljust(jus)}Freq. of popups: {round(random.random(), 2)}\n")"""
    
        output[0] += "\n"
        if random.randint(0, 1): output[0] += "Popups\t"
        if random.randint(0, 1): output[0] += "Level Puzzle\t"
        if random.randint(0, 1): output[0] += "Utilities"
        #output[0] += "\n"
    
    output.extend(os)
    return output

def top_lv(data):
    print("Top Levels")
    tmp = dict(sorted(data.items(), key=lambda m: data[m[0]], reverse=True))
    try:
        del tmp["achivements"]
    except: pass
    
    iterate = list(zip(tmp.items(), ((221, 240, 10), (102, 140, 135), (130, 68, 7), None))) #making it iterable
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
    for n, ((x, y), c) in enumerate(iterate):
        if key == x:
            u = 1
            d_next = f"(Only {val - tmp[pb]} levels to go!)" if dump_ == 0 else ""
        else: d_next = ""
        print(color(f"{x.rjust(l)} - {y} {d_next}", fore=c))
        if pb.startswith("PB NOT") and n == 1: break
    else:
        try:
            if u == 0 and topent != 1 and dump_ == 0: print(f"{key.rjust(l)} - {val} (Only {val - tmp[pb]} levels to go!)")
        except: pass

pro_badge = sort()
d_game, pb, _ = call()
genbar(pb)
if dump_ == 3: pb = list(pro_badge.keys())[0]
lastsys = pb
if dump_ == 3 and dump_: print(f"\n{d_game}")

index = list(pro_badge.keys())
oldperc = round(100.0 * totamt / float(tot), 4)
count = 0

top_lv(data)

while True:



    #print(*[color(f"{x.rjust(l)} - {y}\n", fore=c) for (x, y), c in iterate if y > 0], end = "") #the actual iterating
    
    if dump_ not in (0, 3): break
    inp = input()

    ctrl = "n"
    if inp == "": inp = "+"
    if inp in ("-", "r", "s", "+"): ctrl = inp #setting ctrl var

    try:
        if inp in ("-", "s", "+"): inp = pb #if the input is one of these, have it save the prev. used entry
        else:
             pb = index[int(inp) - 1]
             count = 0
    except ValueError:
        #print(e.__class__.__name__) #the actual error that occured
        if inp == "r": pb = ""
        else: continue

    try:
        if ctrl == "+": data[pb] += 1 #if ctrl isnt set, have it add to data (only properly used for if ctrl is set to skip)
        elif ctrl == "-": data[pb] -= 1 #if ctrl is set to minus, have it subtract
        pass
    except:
        if ctrl == "+" and pb != "": data[pb] = 1 #if there isnt an entry, make one

    with open('pb95.yaml', 'w') as file:
        yaml.dump(data, file)

    pro_badge = sort()

    if not dump_: count += 1
    else: pb = list(pro_badge.keys())[-1]

    try: #get next random entry
        if count >= 3: g_disp, g_os, *_ = call(pb, True) #only allow it to go out of the system after 3 games
        else: g_disp, g_os, *_ = call(pb)
    except:
        pass

    os.system('cls')
    genbar(g_os)
    pb = g_os
    if lastsys != pb:
        count = 0
        lastsys = pb
    print("")

    
    #print(f"levels: {totamt}")

    print(g_disp)    

    newperc = round(100.0 * totamt / float(tot), 4)
    if newperc != oldperc: print(f"{round(newperc - oldperc, 4)}%")
    
    top_lv(data)        
