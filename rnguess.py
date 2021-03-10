import random
import math

min = random.randint(0, 9000)
max = random.randint(min, 9000)
guessn = random.randint(min, max)

print("Guess a number between " + str(min) + " and " + str(max))

print("What is your first guess?")


while True:
    usr = input()

    try:
        #Converts to int
        usr = int(usr)
    except ValueError:
        try:
            #Converts to float
            usr = math.floor(float(usr)) 
            print("Converted your input into int " + usr)
        except ValueError:
            print("Input is not a valid number, please try again")

    if usr < guessn:
        print("Input is below the answer!")
        print("")
        continue

    elif usr > guessn:
        print("Input is above the answer!")
        print("")
        continue
    
    print("Congratulations! The answer was " + str(guessn))
    print("Enter y to play again, or enter to exit")
    usrex = input("y")

    if usrex == "y" or usr == "Y":
        continue
    break

