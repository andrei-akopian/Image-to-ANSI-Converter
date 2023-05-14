import argparse
from PIL import Image
import time
import math
from utils import paletteUtils

startTime=time.time()

ArgumentDefaultsValues={
    "filename":"image.png",
    "contrast":1,
    "sampleSize":"16x16",
    "contrastbreak":128,
    "output":None,
    "blur":30,
    "palettename":None,
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
parser.add_argument("-p","--palettename",default=ArgumentDefaultsValues["palettename"],help="Enter name of the pallete from palettes or file path")
# parser.add_argument("-d","--display", action='store_true', default=False, help="if true (default) will display the image as it is being generated")
args=parser.parse_args()

class ColorPalette: #TODO the pattern probably needs some standartisation
    def __init__(self):
        self.pattern="{ESC}[{foreground}m{ESC}[{background}m"
        self.colorPoints=[]
        self.Raxis=[]
        self.Gaxis=[]
        self.Baxis=[]
        self.muteable=True

    def addpoint(self,point):
        self.colorPoints.append(point)
        self.Raxis.insert(self.search(self.Raxis,point.r,get_val_funk=lambda o: o.r),point)
        self.Gaxis.insert(self.search(self.Gaxis,point.g,get_val_funk=lambda o: o.g),point)
        self.Baxis.insert(self.search(self.Baxis,point.b,get_val_funk=lambda o: o.b),point)
    
    def search(self,axis,target,start=0,end=-1,get_val_funk=lambda o: o.r): #TODO can be improved
        #< target is a numberal
        #binary search to locate the position a point is on the axies
        if end==-1:
            end=len(axis)
        if start==end:
            return start
        elif target>get_val_funk(axis[(start+end)//2]):
            return self.search(axis,target,(start+end)//2+1,end,get_val_funk)
        else:
            return self.search(axis,target,start,(start+end)//2,get_val_funk)

    def ground(self):
        for point in self.colorPoints:
            point.weight=1


class ColorPoint:
    def __init__(self,color):
        self.r=color[0]
        self.g=color[1]
        self.b=color[2]
        self.weight=1
        self.foreground=""
        self.background=""
    def getForeground(self):
        if self.foreground=="":
            return "38;2;"+str(self.r)+";"+str(self.g)+";"+str(self.b)
        else:
            return self.foreground
    def getBackground(self):
        if self.background=="":
            return "48;2;"+str(self.r)+";"+str(self.g)+";"+str(self.b)
        else:
            return self.background
    
    def setContrast(self,contrast,contrastbreak):
        if contrast!=1:
            if 0.33*self.r+0.5*self.g+0.16*self.b>contrastbreak:
                self.r=min(int(self.r*contrast),255)
                self.g=min(int(self.g*contrast),255)
                self.b=min(int(self.b*contrast),255)
            else:
                self.r=min(int(self.r/contrast),255)
                self.g=min(int(self.g/contrast),255)
                self.b=min(int(self.b/contrast),255)

## Adjusters #TODO export this into a different function
# display=args.display
sampleSize=args.sampleSize
if "x" in sampleSize:
    sampleSize=list(map(int,sampleSize.split("x")))
else:
    sampleSize=int(sampleSize)
    sampleSize=[sampleSize,sampleSize]

# Palletes logic
palettename=args.palettename
palette=ColorPalette()
if palettename!=None:
    paletteUtils.loadPalette(palettename,palette,ColorPoint)

sampleParameters = {
    "sampleSize" : sampleSize,
    "contrast" : float(args.contrast),
    "contrastbreak" : int(args.contrastbreak),
    "blur" : int(args.blur)**3,
}

characters="\'^:!=*$%@#" #TODO improve character settings
def selectchar(characters,color0,color1):
    fraction=color1.weight/(color0.weight+color1.weight)
    if fraction<0.5:
        return characters[int(fraction*2*10)]
    return " "

#TODO make filters to filter noise colors
def sample(imgpx,xa,ya,sampleSize,contrast,contrastbreak,blur,palette):
    #sampling
    if palette.muteable:
        palette=ColorPalette()
    else:
        palette.ground()
    for x in range(xa,xa+sampleSize[0]):
        for y in range(ya,ya+sampleSize[1]):
            if x<size[0] and y<size[1]:
                newPoint=ColorPoint(imgpx[x,y])
                #contrast
                newPoint.setContrast(contrast,contrastbreak)
                #main code
                if not(palette.muteable):
                    bestmatch=0
                    bestd=800
                    d=0
                    for i,point in enumerate(palette.colorPoints):
                        d=0
                        d+=abs(point.r-newPoint.r)**2
                        d+=abs(point.g-newPoint.g)**2
                        d+=abs(point.b-newPoint.b)**2
                        d=d**0.5
                        if d<bestd:
                            bestd=d
                            bestmatch=i
                    palette.colorPoints[bestmatch].weight+=1
                else:
                    breakflag=0
                    for point in palette.colorPoints:
                        if calculate_distance(point, newPoint)<blur+point.weight:
                            point.r=(point.r*point.weight+newPoint.r)//(point.weight+1)
                            point.g=(point.g*point.weight+newPoint.g)//(point.weight+1)
                            point.b=(point.b*point.weight+newPoint.b)//(point.weight+1)
                            point.weight+=1
                            breakflag=1
                            break
                    if not(breakflag):
                        palette.addpoint(newPoint)
    #find greatest 2
    maxI=len(palette.colorPoints)-1
    secondMaxI=0
    for i in range(len(palette.colorPoints)):
        if palette.colorPoints[maxI].weight<palette.colorPoints[i].weight:
            secondMaxI=maxI
            maxI=i
        elif palette.colorPoints[secondMaxI].weight<palette.colorPoints[i].weight:
            secondMaxI=i
    return palette.colorPoints[maxI], palette.colorPoints[secondMaxI]

def calculate_distance(point0,point1):
    d=0
    d+=abs(point0.r-point1.r)**2
    d+=abs(point0.g-point1.g)**2
    d+=abs(point0.b-point1.b)**2
    return d**(3/2)/0.24

def find_closest_colorPoint(palette,targetPoint):
    """uses axis data structures in ColorPalette to quickly find closest point
    
    #< palette = ColorPalette
    #< targetPoint = ColorPoint

    #> closestPoint, distance

    After choosing a random point as the "closest so far"
    The furthest a potential closer point could be is directly on a cordinal line less then the distance you already got.
    """
    rpi=palette.search(palette.Raxis,targetPoint,get_val_funk=lambda o: o.r)
    rmi=rpi-1
    gpi=palette.search(palette.Raxis,targetPoint,get_val_funk=lambda o: o.g)
    gmi=gpi-1
    bpi=palette.search(palette.Raxis,targetPoint,get_val_funk=lambda o: o.b)
    bmi=bpi-1
    min_d=800
    closestPoint=None
    n=1
    while n>0:
        n=0 #detect if any changes occured
        if rpi>-1 and rpi<len(Raxis):
            if abs(Raxis[rpi].r-targetPoint.r)<min_d:
                n+=1
                new_d=calculate_distance(Raxis[rpi],targetPoint)
                if new_d<min_d:
                    min_d=new_d
                    closestPoint=Raxis[rpi]
                    rpi=-1
                else:
                    rpi+=1
            else: rpi=-1
        if rmi>-1 and rmi<len(Raxis):
            if abs(Raxis[rmi].r-targetPoint.r)<min_d:
                n+=1
                new_d=calculate_distance(Raxis[rmi],targetPoint)
                if new_d<min_d:
                    min_d=new_d
                    closestPoint=Raxis[rmi]
                    rmi=-1
                else:
                    rmi-=1
            else: rmi=-1
        if gpi>-1 and gpi<len(Gaxis): 
            if abs(Gaxis[gpi].g-targetPoint.g)<min_d:
                n+=1
                new_d=calculate_distance(Gaxis[gpi],targetPoint)
                if new_d<min_d:
                    min_d=new_d
                    closestPoint=Gaxis[gpi]
                    gpi=-1
                else:
                    gpi+=1
            else: gpi=-1
        if gmi>-1 and gmi<len(Gaxis):
            if abs(Gaxis[gmi].g-targetPoint.g)<min_d:
                n+=1
                new_d=calculate_distance(Gaxis[gmi],targetPoint)
                if new_d<min_d:
                    min_d=new_d
                    closestPoint=Gaxis[gmi]
                    gmi=-1
                else:
                    gmi-=1
            else: gmi=-1
        if bpi>-1 and bpi<len(Baxis): 
            if abs(Baxis[bpi].b-targetPoint.b)<min_d:
                n+=1
                new_d=calculate_distance(Baxis[bpi],targetPoint)
                if new_d<min_d:
                    min_d=new_d
                    closestPoint=Baxis[bpi]
                    bpi=-1
                else:
                    bpi+=1
            else: bpi=-1
        if bmi>-1 and bmi<len(Baxis):
            if abs(Baxis[bmi].b-targetPoint.b)<min_d:
                n+=1
                new_d=calculate_distance(Baxis[bmi],targetPoint)
                if new_d<min_d:
                    min_d=new_d
                    closestPoint=Baxis[bmi]
                    bmi=-1
                else:
                    bmi+=1
            lse: bmi=-1
    return closestPoint, distance
                

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
        color0, color1=sample(imgpx,xa,ya,**sampleParameters,palette=palette)
        line+=palette.pattern.format(ESC="\033",foreground=color0.getForeground(),background=color1.getBackground())
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
