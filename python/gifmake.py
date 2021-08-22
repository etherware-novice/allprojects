import sys, getopt, os, re
from PIL import Image

path = os.path.abspath(f"{os.getcwd()}\{sys.argv[1]}")

images = []
args = [sys.argv[2]]

if not os.path.exists(path):
    path = os.getcwd()

try:
    args.append(sys.argv[3])
except: pass

    
def search(pre:str = "", post:str = ""):
    for x in range(0, 4):
        y = str(0).rjust(x, "0")
        if os.path.isfile(f"{path}\\{pre}{y}{post}"): 
            n = 0
            break
    else: n = 1
    pre = f".*{pre}" if pre != "" else pre
    for x in os.listdir(path):
        if re.match(f"^{pre}0*{n}{{1}}{post}.png", x) != None: 
            yield x
            n += 1
        #if re.match(f"^{pre}", x): yield x


for x in search(*args):
    print(f"Appending file {x}")
    im = Image.open(f"{path}\{x}")
    images.append(im)

fin = images[-1]
print("Filling in ending frames....")
for x in range(0, 48):
    images.append(fin)
print("Done.")


images[0].save('output.gif', format="gif", save_all=True, append_images=images[1:], loop=0, optimize = True, duration=41.66) #converts the list to a gif