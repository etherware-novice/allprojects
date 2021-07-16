from PIL import Image, ImageDraw, ImageFont
import io, math, textwrap

images = [] #list that will be made into gif
#font = ImageFont.truetype(r'C:\Windows\Fonts\dosapp.ttf', 20) 
font = ImageFont.truetype("PressStart2P-Regular.ttf", 48) #the ttf font used

template = Image.open('temp.png') #opens the stream of the template

with open("line.txt", "r") as f:
    prompts = f.read().splitlines() #gets lines from line.txt

for x in prompts: #for every entry in the list
    im = Image.new('RGBA', (632, 412), (255, 255, 255, 0)) #creates a transparant image
    tmp = template.copy() #copies the template to not modif the original stream
    d = ImageDraw.Draw(im) #gets drawing object out of the im object

    
    #buffer = io.BytesIO() 
    wrapper = textwrap.TextWrapper(width=12) #gets a text wrapper with max length of 12 (basically an object to wrap text)
    x = wrapper.fill(text=x) #returns the string of x with \n to keep it in the textwrapper

    d.multiline_text((310, 190), #anchors the text around the mid of the smaller image
    x, #string
    font = font, #uses the font from earlier
    anchor = "mm", #anchor of middle (for x coord) and baseline (for y coord)
    align="center", #text aligning
    fill = (61, 99, 196)) #color align

    tmp.paste(im, (154, 312)) #puts the text image in the correct place on the template img

    images.append(tmp)



        

images[0].save('output.gif', format="gif", save_all=True, append_images=images[1:], loop=0, optimize = True, duration=41.66) #converts the list to a gif