import random


baseline = ["Relax", "Normal", "Hardcore"]
default = baseline + ["Progress Sweeper", "Progress Defender"] #relax, normal, hardcore, sweeper, defender
bonus = default + ["ProgressDOG", "Matrix", "3DSavr"] #relax, normal, hardcore, sweep, def, pbstein, matrix, savr
probonus = bonus + ["PBXL"]

baselineBAR = ["Casual", "Regular", "High-End"]
bonusBAR = baselineBAR + ["Color", "Jigsaw Puzzle"]

global dict
dict = {
    "PB-DOS": ["Relax", "Normal", "Hardcore", "Knockoff Tetris", "Progress Commander"],
    "PB1": default,
    "PB2": default,
    "PB 3.14": bonus,
    "Chitown": ["Normal"],
    "PB95": [x for x in bonus + ["Progress Commander"] if x not in ("Relax", "Hardcore", "Progress Defender")], #look this is already incredibly messy ok-
    "PB95+": [x for x in probonus + ["Progress Commander"] if x not in ("Hardcore")],
    "PB NOT 4.0": ["Custom"],
    "PB98": probonus + ["Progress Commander"],
    "MEME": probonus,
    "PB2000": probonus,
    "Whisper": bonus,
    "XB": probonus,
    "Largehorn": bonus,
    "Wista": probonus,
    "7": probonus,
    "81": probonus,
    "10": default + ["ProgressDOG"],
    "1X": default + ["ProgressDOG"],
    "B1": ["Regular"],
    "B2": ["Casual", "Regular"],
    "B3": baselineBAR,
    "B4": baselineBAR,
    "B5": baselineBAR,
    "B6": baselineBAR,
    "B7": bonusBAR,
    "B8": bonusBAR,
    "B9": bonusBAR,
    "B10": bonusBAR,
    "B10.2": bonusBAR,
    "B10.3": bonusBAR,


    "PB NOT 3.60": ["Custom"] #delete this after testing
}

def call(curr:str = "", out = False):
    gamem = None
    output = [""]
    try:
        if out == True and random.randint(0, 2) == 0: raise KeyError("lol ignore this")
        else:
            gamem = random.choice(dict[curr])
            os = [curr, gamem]
            output[0] = f"{curr} - {gamem}"
    except KeyError:
        os = random.choice(list(dict.items()))
        gamem = random.choice(os[1])
        #os[1] = gamem
        output[0] = f"{os[0]} - {gamem}"


    if gamem == "Custom":
        output[0] += "\n"
        jus = 20
        output[0] += (f"Pace: {str(round(random.random(), 2)).ljust(jus)}Segments Speed: {round(random.random(), 2)}\n"
        f"Segment Wobble: {str(round(random.random(), 2)).ljust(jus)}Wobble Speed: {round(random.random(), 2)}\n"
        f"Freq. of Red: {str(round(random.random(), 2)).ljust(jus)}Freq. of popups: {round(random.random(), 2)}\n")
    
        if random.randint(0, 1): output[0] += "Popups\t"
        if random.randint(0, 1): output[0] += "Level Puzzle\t"
        if random.randint(0, 1): output[0] += "Utilities"
    
    output.extend(os)
    return output

def get_os():
    return random.choice(list(dict.keys()))
    
