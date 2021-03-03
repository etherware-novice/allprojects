#Copyright by candycane (not really but dont steal)
# you will have to manually copy the images from images-c to undo this for now (i will make it automatic in a future update)

#--USER SECTION--#
# PLEASE PUT IN YOUR DIRECTORY LOCATION HERE OR ELSE IT WILL NOT WORK!!!!!!!
#also you can change the files that are affected here if you want to screw the game up even more

file = "C:/Users/server/Downloads/funkin-windows-64bit"
#put the base directory for fnf here (the folder that has fnf.exe in it)
#also you need to manually replace \'s with /'s in the path or else it wont work

filenames = ["BOYFRIEND", "campaign_menu_UI_assets", "campaign_menu_UI_characters", "combo", "DADDY_DEAREST", "FNF_main_menu_assets", "GF_assets", "gfDanceTitle", "go", "good", "grafix", "halloween_bg", "healthBar", "iconGrid", "logo", "logoBumpin", "menuBG", "menuBGBlue", "menuBGMagenta", "menuDesat", "Mom_Assets", "newgrounds_logo", "num0", "num1", "num2", "num3", "num4", "num5", "num6", "num7", "num8", "num9", "Pico_FNF_assetss", "ready", "set", "shit", "sick", "spooky_kids_assets", "stage_light", "stageback", "stagecurtains", "stagefront", "titleEnter"]
#this controlls what files in assets/images are affected, feel free to change it if you want to keep certain images or throw in unused ones

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
if os.path.isdir(file + "/assets/images"): print("Install: OK") #checking that the base images folder exists
else:
    print("The install folder you have inserted does not seem to be working. Please insert a valid path and try again")
    input(exitp)
    sys.exit()

if os.path.isdir(file + "/assets/images-c"): #checking the backup image folder exists
    print("Backup Images: OK")
    
else: #request to make new folder
    print("Backup images folder not found, would you like to create one?")
    tmp = input("(Y/N): ")
    if tmp == "Y" or tmp == "y":
        copydir(file + "/assets/images", file + "/assets/images-c")
        print("Folder created")
    elif tmp == "N" or tmp == "n":
        print("The backup folder is needed for the program to run properly, so operation can not go forward.")
        input(exitp)
        sys.exit()

print("")
####################################
# setting up the counter for later #
####################################

count = []
i = 0
while i < len(filenames):
    count.append(i)
    i += 1    
    
#creates the "mapping" setup for how files end up getting renamed (as in the first entry in filenames would be renamed to whatever this list points to in filenames. However, the list isnt shuffled yet

"""x = 0
y = 0
for x in filenames:
    rand = random.randint(0, 44)
 
print(rand)"""


#########################
# shuffling the counter #
#########################

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
    shuffle(count)
    x += 1

print("File mapper sorted")

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

while i < len(filenames):
    orig = file + "/assets/images-c/" + filenames[i] + ".png" #getting the full path of the image to copy (alphabetical)
    newname = file + "/assets/images/" + filenames[count[i]] + ".png" #getting the full path of the new image name(random)
    shutil.copyfile(orig, newname) #copies the image to the main images folder
    i += 1 
    # perc = round(round(i / len(filenames), 3) * 100, 3) 
    perc = formatNumber(round(i / len(filenames) * 100, 2)) #this basically calculates the percentile of images completed
    print("\r" + str(perc) + " percent done    ", end="") #displays the previous percentile calculation with extra text
    time.sleep(0.05) #this slows it down just slightly so you can actually appreciate this
 
print("\n")
#figure out a goddange way to create affected.txt
#txt = open(file + "/assets/image/affected.txt", 'w')
#text.write("test")
