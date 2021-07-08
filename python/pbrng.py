import random


baseline = ["Relax", "Normal", "Hardcore"]
default = baseline + ["Progress Sweeper", "Progress Defender"]
bonus = default + ["ProgressDOG", "Matrix", "3DSavr"]
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
    "PB95": bonus,
    "PB95+": probonus + ["Progress Commander"],
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
    "B10.3": bonusBAR
}

def call(curr:str = "", out = False):
    try:
        if out == True and random.randint(0, 2) == 0: raise ValueError("lol ignore this")
        else:
            print(f"{curr} - {random.choice(dict[curr])}")
    except KeyError:
        os = random.choice(list(dict.items()))
        print(f"{os[0]} - {random.choice(os[1])}")
