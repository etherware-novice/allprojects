import pyperclip

#string
message = "This is my secret message"

#encrypt key
key = 13

#encrypt and decrypt switch
mode = 'encrypt'

#Possible symbols that can be encrypted
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

#stores the translated message
translated = ''

#capitalize the string
message = message.upper()

#run the code on each symbol
for symbol in message:
    if symbol in LETTERS:
        #get the encrypted number for the symbol
        num = LETTERS.find(symbol) #gets the number of the symbol
        if mode == 'encrypt':
            num = num + key
        elif mode == 'decrypt':
            num = num - key

        #handle wraparound if num is larger than letters or less than 0
        if num >= len(LETTERS):
            num = num - len(LETTERS)
        elif num < 0:
            num = num + len(LETTERS)

        #add encrypted numbers symbol at end of translated
        translated = translated + LETTERS[num]

    else:
        #add symbol without encrypting
        translated = translated + symbol

print(translated)
