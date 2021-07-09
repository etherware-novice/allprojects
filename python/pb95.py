import yaml
import math
from colr import color
import os
try:
    import pbrng #custom rng file
except:
    print("pbrng module not found")

data = None


pro_badge = {
    "PB-DOS": 10,
    "PB1": 10,
    "PB2": 10,
    "PB 3.14": 10,
    "PB NOT 3.60": 10,
    "Chitown": 10, #lets pray these are accurate
    "PB95": 10, #indir
    "PB95+": 20, #indir
    "PB NOT 4.0": 30, #confirmed
    "PB98": 20, #indir
    "MEME": 30, #indir
    "PB2000": 30, #indir
    "Whisper": 30, #indir
    "XB": 30, #indir
    "Largehorn": 60, #confirmed,
    "Wista": 40, #indir
    "7": 40, #indir
    "81": 50, # (frick i already got expert)
    "10": 50, #confirmed also what??
    "1X": 60,

    #barOS
    "B1": 10,
    "B2": 20,
    "B3": 30,
    "B4": 40, #confirmed
    "B5": 50, #confirmed
    "B6": 60, #confirmed
    "B7": 60, #semi confirmed
    "B8": 70, #confirmed
    "B9": 70, #confirmed
    "B10": 70, #confirmed
    "B10.2": 70, #confirmed
    "B10.3": 70, #confirmed

    #"achivements": 86

    #60
}

#expert - 100
#master - 250



barbg = (8, 35, 70)
x = 0
def progress(count, total, bar_len, percent=False):

    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)

    displpercent = ""
    if percent: displpercent = percents
    return color('=' * filled_len, back=barbg) + '-' * (bar_len - filled_len) + " " + str(displpercent)

global totamt, tot, levels
def genbar(newc = None):
    x = 0
    
    global data
    with open(r'pb95.yaml') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)

    #data['PB NOT 3.60'] = 0
    global totamt
    global tot
    global levels
    totamt = 0
    tot = 0
    levels = 0

    for sys, pro in pro_badge.items():
        pbar = "".ljust(25, "-") #each dash = 10` points
        #global totamt, tot, levels

        try:
            prog = math.floor(data[sys] / 5) 
            pbar = pbar.replace("-", "=", math.ceil(prog / 2)) #replaces all the thing that itdoes
            if prog % 2 == 1:
                pbar = pbar[::-1].replace("=", "/", 1)[::-1] #replaces last occurance of = with /
            prog = math.ceil(prog / 2) #returns the amount of things were affected
            rawprog = data[sys]

        except:
            rawprog = prog = 0
        
        pbar = list(pbar)

        nextgoal = pro
        nextlbl = ""
        if rawprog >= nextgoal: 
            nextgoal = 100 
            nextlbl = "(pro)"
        if rawprog >= nextgoal:
            nextgoal = 250
            nextlbl = "(expert)"
        if rawprog >= nextgoal:
            nextgoal = -1
            nextlbl = "(master)"

    
        


        #setting up the labels
        prolabl = 0
        if pro != 10: prolabl = round((pro / 10) - 1)
        """if sys == "achivements": #spec case for achivements bar
            sys = "\n" + sys
            pbar[-1] = "F"
            nextgoal = "86"
            nextlbl = ""
        """
        pbar[prolabl] = "P" #pro badge label
        pbar[9] = "E" #expert badge label
        pbar[24] = "M" #expert badge label

        if nextgoal >= 0: numprog = f"{str(rawprog).rjust(3)} / {str(nextgoal).ljust(5)} {nextlbl}"
        else: numprog = f"{str(rawprog).rjust(9)} {nextlbl.rjust(10)}"


        if prog != 0:
            colored = "".join(pbar[:prog]) #colored section required to replaec
            del pbar[:prog]
            colored = color(colored, back=barbg)
            pbar.insert(0, colored)
        
        pbar = "".join(pbar)

        tot += 250
        totamt += rawprog    

        l = len(max(pro_badge.keys(), key=len))
        if sys == "B1": 
            print('\n')
            print('BarOS:'.rjust(l + 1))
        ffs = "-"
        sysp = sys.rjust(l, ffs)

        
        ent = f"{str(x + 1).rjust(2).ljust(4, ffs)}{sysp}: {pbar}  {numprog.rjust(7)}"
        if newc != None and sys == newc: ent += color(" <--- NEW", fore=(52, 227, 78))
        print(ent)

        x += 1

    levels = totamt

    ach = "achivements"
    ach = ach.rjust(l).ljust(10)

    achamt = 86
    try:
        data2 = data["achivements"]
        numprog = f"{str(data2).rjust(3)} / {achamt}"
        print(f"\n{str(x + 1).rjust(2).ljust(3)} {ach}: {progress(data2, achamt, 25)} {numprog}")
        totamt += data2
    except:
        print(f"{str(x + 1).rjust(2).ljust(4)} {ach}: {progress(0, 1, 25)}    0 / {achamt}")
    tot += achamt

    ach = "total".rjust(l + 3)
    print(f"\n {ach}: {progress(totamt, tot, 30, True)}")

index = list(pro_badge.keys())
index.append('achivements')

sys = pbrng.get_os()
genbar(sys)
print("\n")
print(pbrng.call(sys)[0])

count = 0

oldperc = round(100.0 * totamt / float(tot), 4)
while True:
    inp = input("")

    data["PB NOT 3.60"] = 0

    ctrl = "n"
    if inp == "": inp = "+"
    if inp in ("-", "r", "s", "+"): ctrl = inp #setting ctrl var

    try:
        if inp in ("-", "s", "+"): inp = sys #if the input is one of these, have it save the prev. used entry
        else:
             sys = index[int(inp) - 1]
             count = 0
    except ValueError:
        #print(e.__class__.__name__) #the actual error that occured
        if inp == "r": sys = ""
        else: continue
    
    try:
        if ctrl == "+": data[sys] += 1 #if ctrl isnt set, have it add to data (only properly used for if ctrl is set to skip)
        elif ctrl == "-": data[sys] -= 1 #if ctrl is set to minus, have it subtract
        pass
    except:
        if ctrl == "+" and sys != "": data[sys] = 1 #if there isnt an entry, make one
    
    with open('pb95.yaml', 'w') as file:
        yaml.dump(data, file)
    
    count += 1
    
    try: #get next random entry
        if count >= 3: gener = pbrng.call(sys, True) #only allow it to go out of the system after 3 games
        else: gener = pbrng.call(sys)
    except:
        pass

    os.system('cls')
    genbar(gener[1])
    sys = gener[1]
    print("\n")

    
    print(f"levels: {levels}")

    print(gener[0])    

    newperc = round(100.0 * totamt / float(tot), 4)
    if newperc > oldperc: print(f"+{round(newperc - oldperc, 4)}%")