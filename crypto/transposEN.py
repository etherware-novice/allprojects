def main():
    myMessage = 'Common Sense is not so common'
    myKey = 8

    ctext = encryptMessage(myKey, myMessage)

    print(ctext + '<')


def encryptMessage(key, message):
    # Each string in ciphertext represents a column in grid
    ciphertext = [''] * key

    for col in range(key):
        pointer = col

        while pointer < len(message):
            ciphertext[col] += message[pointer]

            pointer += key

    return ''.join(ciphertext)

if __name__ == '__main__':
    main()
