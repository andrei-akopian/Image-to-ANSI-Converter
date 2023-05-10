from PIL import Image
import time
import math
startTime=time.time()

## Adjusters
# display=args.display
blur=int(args.blur)**3
contrast=float(args.contrast)
contrastbreak=int(args.contrastbreak)

sampleSize=args.sampleSize
if "x" in sampleSize:
    sampleSize=list(map(int,sampleSize.split("x")))
else:
    sampleSize=int(sampleSize)
    sampleSize=[sampleSize,sampleSize]

characters="\'^:!=*$%@#"
def selectchar(characters,color0,color1):
    fraction=color1[1]/(color0[1]+color1[1])
    if fraction<0.5:
        return characters[int(fraction*2*10)]
    return " "

#TODO make filters to filter noise colors
def sample(imgpx,xa,ya,sampleSize,contrast,contrastbreak=128,blur=125000):
    #parse
    pointList=[] # tuples [color,multiplier]
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
                breakflag=0
                for oldPoint in pointList:
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
                    pointList.append(newPoint)

    maxI=len(pointList)-1
    secondMaxI=0
    for i in range(len(pointList)):
        if pointList[maxI][1]<pointList[i][1]:
            secondMaxI=maxI
            maxI=i
        elif pointList[secondMaxI][1]<pointList[i][1]:
            secondMaxI=i
    return pointList[maxI], pointList[secondMaxI]

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
        color0, color1 =sample(imgpx,xa,ya,sampleSize,contrast,contrastbreak,blur)
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
