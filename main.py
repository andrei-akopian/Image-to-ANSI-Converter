import argparse
from PIL import Image
import time
import math
from utils import paletteUtils

ArgumentDefaultsValues={
    "filename":"image.png",
    "contrast":1,
    "sampleSize":"16x16",
    "contrastbreak":128,
    "output":None,
    "blur":30,
    "palette":None,
}

#parse cli arguments
parser=argparse.ArgumentParser(
    prog="Image to ANSI converter"
)

parser.add_argument("-f","--filename",default=ArgumentDefaultsValues["filename"],help="Filepath to your image, the default image name is image.png")
parser.add_argument("-c","--contrast",default=ArgumentDefaultsValues["contrast"],help="allows you to change the contrast of the image for better results. (recomended 1 - 1.2 range)")
parser.add_argument("-s","--sampleSize",default=ArgumentDefaultsValues["sampleSize"],help="Size of the samples, default is 16x16 (the output will be 16x smaller) enter as XxY or just X")
parser.add_argument("-cb","--contrastbreak",default=ArgumentDefaultsValues["contrastbreak"],help="Border of darkness levels between making a pixel darker or brighter (0-255 recomended range 50-200)")
parser.add_argument("-o","--output",default=ArgumentDefaultsValues["output"],help="Specify output file it can be then displayed with `cat output.txt` with all the colors")
parser.add_argument("-b","--blur",default=ArgumentDefaultsValues["blur"],help="Blurs a furhter range of colors")
parser.add_argument("-p","--palette",default=ArgumentDefaultsValues["palette"],help="Enter name of the pallete from palettes or file path")
# parser.add_argument("-d","--display", action='store_true', default=False, help="if true (default) will display the image as it is being generated")
args=parser.parse_args()

# with open("converter.py","r") as f:
#     code=f.read()
# exec(compile(code,"converter","exec"))

startTime=time.time()


anchorColors=[]
## Adjusters #TODO export this into a different function
# display=args.display
sampleSize=args.sampleSize
if "x" in sampleSize:
    sampleSize=list(map(int,sampleSize.split("x")))
else:
    sampleSize=int(sampleSize)
    sampleSize=[sampleSize,sampleSize]

# Palletes logic
palette=args.palette
usePalette=False
if palette!=None:
    usePalette=True
    palette, anchorColors=paletteUtils.loadPalette(palette)

sampleParameters = {
    "sampleSize" : sampleSize,
    "contrast" : float(args.contrast),
    "contrastbreak" : int(args.contrastbreak),
    "blur" : int(args.blur)**3,
    "usePalette" : usePalette
}

characters="\'^:!=*$%@#"
def selectchar(characters,color0,color1):
    fraction=color1[1]/(color0[1]+color1[1])
    if fraction<0.5:
        return characters[int(fraction*2*10)]
    return " "

#TODO make filters to filter noise colors
def sample(imgpx,xa,ya,sampleSize,contrast,contrastbreak,blur,usePalette,anchorColors=[]):
    #sampling
    if not(usePalette):
        anchorColors=[]
    else:
        for c in anchorColors:
            c[1]=1
    for x in range(xa,xa+sampleSize[0]):
        for y in range(ya,ya+sampleSize[1]):
            if x<size[0] and y<size[1]:
                newPoint=[list(imgpx[x,y]),1]
                #contrast
                if contrast!=1:
                    if 0.33*newPoint[0][0]+0.5*newPoint[0][1]+0.16*newPoint[0][2]>contrastbreak:
                        newPoint[0][0]=min(int(newPoint[0][0]*contrast),255)
                        newPoint[0][1]=min(int(newPoint[0][1]*contrast),255)
                        newPoint[0][2]=min(int(newPoint[0][2]*contrast),255)
                    else:
                        newPoint[0][0]=min(int(newPoint[0][0]/contrast),255)
                        newPoint[0][1]=min(int(newPoint[0][1]/contrast),255)
                        newPoint[0][2]=min(int(newPoint[0][2]/contrast),255)
                #main code
                if usePalette:
                    bestmatch=0
                    bestd=800
                    d=0
                    for i,color in enumerate(anchorColors):
                        for c in range(3):
                            d+=abs(color[0][c]-newPoint[0][c])**2
                        d=d**0.5
                        if d<bestd:
                            bestd=d
                            bestmatch=i
                    anchorColors[bestmatch][1]+=1
                else:
                    breakflag=0
                    for oldPoint in anchorColors:
                        d=0
                        for c in range(3):
                            d+=abs(newPoint[0][c]-oldPoint[0][c])**2
                        if d<((blur+oldPoint[1])*0.24)**(2/3):
                            for c in range(3):
                                oldPoint[0][c]=(oldPoint[0][c]*oldPoint[1]+newPoint[0][c])//(oldPoint[1]+1)
                            oldPoint[1]+=1
                            breakflag=1
                            break
                    if not(breakflag):
                        anchorColors.append(newPoint)
    #find greatest 2
    maxI=len(anchorColors)-1
    secondMaxI=0
    for i in range(len(anchorColors)):
        if anchorColors[maxI][1]<anchorColors[i][1]:
            secondMaxI=maxI
            maxI=i
        elif anchorColors[secondMaxI][1]<anchorColors[i][1]:
            secondMaxI=i
    return anchorColors[maxI], anchorColors[secondMaxI], maxI, secondMaxI

img = Image.open(args.filename)
imgpx = img.load()
size=img.size

outputFile=args.output
outputContent=[]

print("Original Size:",size[0],size[1],"px")
print("ANSI Size:",math.ceil(size[0]/sampleSize[0]),math.ceil(size[1]//sampleSize[1]),"chr")
print("Estimated Runtime:",len(anchorColors)*size[0]*size[1]//100000/20,"s at 2M op/s")

for ya in range(0,size[1],sampleSize[1]):
    line=""
    for xa in range(0,size[0],sampleSize[0]):
        if usePalette:
            color0, color1, color0i, color1i =sample(imgpx,xa,ya,**sampleParameters,anchorColors=anchorColors)
            line+=palette["pattern"].format(ESC="\033",foreground=palette["colors"][color0i][0],background=palette["colors"][color1i][1])
            line+=selectchar(characters, color0, color1)
        else:
            color0, color1, _, _ =sample(imgpx,xa,ya,**sampleParameters)
            line+="\033[48;2;"+str(color0[0][0])+";"+str(color0[0][1])+";"+str(color0[0][2])+"m"
            line+="\033[38;2;"+str(color1[0][0])+";"+str(color1[0][1])+";"+str(color1[0][2])+"m"
            line+=selectchar(characters, color0, color1)
    line+="\n"
    outputContent.append(line)
    # if display:
    print(line,end="")

if outputFile!=None:
    with open(outputFile,"w") as f:
        for line in outputContent:
            f.write(line)

print("\033[0mConverstion Time:",time.time()-startTime,"s")
