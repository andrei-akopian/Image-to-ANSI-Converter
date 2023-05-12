from PIL import Image
import time
import math
from utils import paletteUtils
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
def selectchar(characters,anchorColors,color0i,color1i):
    fraction=anchorColors[color1i][1]/(anchorColors[color0i][1]+anchorColors[color1i][1])
    if fraction<0.5:
        return characters[int(fraction*2*10)]
    return " "

#TODO make filters to filter noise colors
def sample(imgpx,xa,ya,anchorColors,sampleSize,contrast,contrastbreak,blur,usePalette):
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
    return maxI, secondMaxI, anchorColors #FIXME fix this mess with imports

img = Image.open(args.filename)
imgpx = img.load()
size=img.size

outputFile=args.output
outputContent=[]

print("Original Size:",size[0],size[1],"px")
print("ANSI Size:",math.ceil(size[0]/sampleSize[0]),math.ceil(size[1]//sampleSize[1]),"chr")

for ya in range(0,size[1],sampleSize[1]):
    line=""
    for xa in range(0,size[0],sampleSize[0]):
        color0i, color1i, anchorColors =sample(imgpx,xa,ya,anchorColors,**sampleParameters)
        if usePalette:
            line+=palette["pattern"].format(ESC="\033",foreground=palette["colors"][color0i][0],background=palette["colors"][color1i][1])
        else:
            line+="\033[48;2;"+str(anchorColors[color0i][0][0])+";"+str(anchorColors[color0i][0][1])+";"+str(anchorColors[color0i][0][2])+"m"
            line+="\033[38;2;"+str(anchorColors[color1i][0][0])+";"+str(anchorColors[color1i][0][1])+";"+str(anchorColors[color1i][0][2])+"m"
        line+=selectchar(characters, anchorColors, color0i, color1i)
    line+="\n"
    outputContent.append(line)
    # if display:
    print(line,end="")

if outputFile!=None:
    with open(outputFile,"w") as f:
        for line in outputContent:
            f.write(line)

print("\033[0mConverstion Time:",time.time()-startTime,"s")
