import json




data = {"test1": 1, "test2": 2, "test3": 3, "new_key": 4} #assigns data to be used for overriding


class jsonfile(object):
    """docstring for jsonfile"""
    def __init__(self, file): #file is an actual argument
        super(jsonfile, self).__init__() #idk what this does but i feel like it might break if i remove
        self.file = file #makes the argument file a class var

        try: 
            with open(file) as file: #attempts to load the file that was inputted
                self.data = file_contents = json.load(file) # parses the JSON data in the file and returns a dictionary assigned to class var data
        except: #if the file doesnt exist yet
            open(file, "x") # creates the file
            print(f'{file} was not found, creating...') #flavortext
            self.data = {} #still makes sure data exists to not error out


    def write(self, input): #overrides the json with input
        with open(self.file, "w") as file: #opens up the file for writing
            file.write(json.dumps(input, indent=4)) # formats and beautifies the JSON as a string and overwrites the file contents with it
        self.data = input #updates the data var to make sure its uptodate
    
foo = jsonfile('file.json')

print(foo.data)
foo.write(data)
print(foo.data)
print(foo.file)