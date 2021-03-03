#Copyright by candycane (not really but dont steal)
# you will have to manually copy the images from music-c to undo this for now (i will make it automatic in a future update)

#--USER SECTION--#
# PLEASE PUT IN YOUR DIRECTORY LOCATION HERE OR ELSE IT WILL NOT WORK!!!!!!!
#also you can change the files that are affected here if you want to screw the game up even more

file = "C:/Users/server/Downloads/funkin-windows-64bit - anime"
#put the base directory for fnf here (the folder that has fnf.exe in it)
#also you need to manually replace \'s with /'s in the path or else it wont work

inst = ["Blammed_Inst", "Bopeebo_Inst", "breakfast", "Cocoa_Inst", "Dadbattle_Inst", "Eggnog_Inst", "freakyMenu", "Fresh_Inst", "gameOver", "gameOverEnd", "gameOverEnd-pixel", "High_Inst", "Milf_Inst", "Monster_Inst", "Philly_Inst", "Pico_Inst", "Roses_Inst", "Satin-Panties_Inst", "Senpai_Inst", "South_Inst", "Spookeez_Inst", "Test_Inst", "Thorns_Inst", "Tutorial_Inst", "Winter-Horrorland_Inst"]
vo = ["Blammed_Voices", "Bopeebo_Voices", "Cocoa_Voices", "Dadbattle_Voices", "Eggnog_Voices", "Fresh_Voices", "High_Voices", "Milf_Voices", "Monster_Voices", "Philly_Voices", "Pico_Voices", "Roses_Voices", "Satin-Panties_Voices", "Senpai_Voices", "South_Voices", "Spookeez_Voices", "Test_Voices", "Thorns_Voices", "Winter-Horrorland_Voices"]

#--USER SECTION END--#

###############
# import hell #
###############:

import time
import random
from random import seed
from random import randint
from random import shuffle
import os.path
from os import path
import sys
import shutil
import math
import subprocess

def formatNumber(num):
  if num % 1 == 0:
    return int(num)
  else:
    return num
    
def copydir(src, des):
    try: 
            shutil.copytree(src, des) 
    except OSError as err: 
        # error caused if the source was not a directory 
            if err.errno == errno.ENOTDIR: 
                shutil.copy2(src, dest) 
            else: 
                print("Error: % s" % err) 
exitp = "Press enter to terminate the program"



# generate new seed
# basically this is just getting a random number and setting it as the rng seed. im doing this bc its impossible to tell what the seed is without setting it manually and then its not random anymore so this was the next best thing
seed = random.randint(0,999999999)
random.seed(seed)


##########################
# source folder checking #
##########################
if os.path.isdir(file + "/assets/music"): print("Install: OK") #checking that the base images folder exists
else:
    print("The install folder you have inserted does not seem to be working. Please insert a valid path and try again")
    input(exitp)
    sys.exit()

if os.path.isdir(file + "/assets/music-c"): #checking the backup image folder exists
    print("Backup Images: OK")
    
else: #request to make new folder
    print("Backup images folder not found, would you like to create one?")
    tmp = input("(Y/N): ")
    if tmp == "Y" or tmp == "y":
        copydir(file + "/assets/music", file + "/assets/music-c")
        print("Folder created")
    elif tmp == "N" or tmp == "n":
        print("The backup folder is needed for the program to run properly, so operation can not go forward.")
        input(exitp)
        sys.exit()



# setting up the mapper (or at least i think?)

instarr = []
voarr = []
i = 0
while i < len(inst):
    instarr.append(i)
    i += 1    

i = 0
while i < len(vo):
    voarr.append(i)
    i += 1
    
# extremely fancy shuffle thing
#imma be honest, this part is completely redundant, im just too lazy to remove it
#basically whats happening here is that im getting 2 random numbers between 0 and 500, and if x is greater than y, it gets a new set. Then, it shuffles the counter every time x increments until it equals y

x = random.uniform(0, 500)
y = random.uniform(0, 500)

while x > y:
    x = random.uniform(0, 500)
    y = random.uniform(0, 500)
    
print("Seed: " + str(seed))
print(str(math.floor(y - x)) + " shuffles to do")
   
while x < y:
    shuffle(instarr)
    x += 1

print("Instrumental mapper sorted")

#vo map
x = random.uniform(0, 500)
y = random.uniform(0, 500)

while x > y:
    x = random.uniform(0, 500)
    y = random.uniform(0, 500)
    
print(str(math.floor(y - x)) + " shuffles to do")
   
while x < y:
    shuffle(voarr)
    x += 1

print("VO mapper sorted")

################################
# actually doing the shuffling #
################################

#heres the fun part

i = 0

"""
print("\nDEBUG MODE: NOT AFFECTING FILES")
print("Files affected: \n")
while i < len(filenames):
    print(filenames[i] + " --> " + filenames[count[i]])
    i += 1
"""

#inst mixer
while i < len(inst):
    orig = file + "/assets/music-c/" + inst[i] + ".ogg" #getting the full path of the image to copy (alphabetical)
    newname = file + "/assets/music/" + inst[instarr[i]] + ".ogg" #getting the full path of the new image name(random)
    shutil.copyfile(orig, newname) #copies the image to the main images folder
    i += 1 
    # perc = round(round(i / len(filenames), 3) * 100, 3) 
    perc = formatNumber(round(i / len(inst) * 100, 2)) #this basically calculates the percentile of images completed
    print("\r" + str(perc) + " percent done   (Instrumental) ", end="") #displays the previous percentile calculation with extra text
    time.sleep(0.05) #this slows it down just slightly so you can actually appreciate this
 
 
i = 0
while i < len(vo):
    orig = file + "/assets/music-c/" + vo[i] + ".ogg" #getting the full path of the image to copy (alphabetical)
    newname = file + "/assets/music/" + vo[voarr[i]] + ".ogg" #getting the full path of the new image name(random)
    shutil.copyfile(orig, newname) #copies the image to the main images folder
    i += 1 
    # perc = round(round(i / len(filenames), 3) * 100, 3) 
    perc = formatNumber(round(i / len(vo) * 100, 2)) #this basically calculates the percentile of images completed
    print("\r" + str(perc) + " percent done   (Voice)      ", end="") #displays the previous percentile calculation with extra text
    time.sleep(0.05) #this slows it down just slightly so you can actually appreciate this
 
print("\n")