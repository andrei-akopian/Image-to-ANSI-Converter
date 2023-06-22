from PIL import Image
import yaml
from utils import colorUtils, cliparser, outputUtils, debugInfoUtils

def parseParameters(arguments):
    #sample size
    sampleSize=arguments.sampleSize
    if "x" in sampleSize:
        sampleSize=list(map(int,sampleSize.split("x")))
    else:
        sampleSize=int(sampleSize)
        sampleSize=[sampleSize,sampleSize]

    #Create/load palette
    palettename=arguments.palettename
    palette=colorUtils.ColorPalette()
    if palettename!=None:
        colorUtils.loadPalette(palettename,palette)

    #characters
    characters=arguments.characters
    characterfile=arguments.characterfile
    if characterfile!=None:
        with open(characterfile,"r") as f:
            characters=f.read().strip("\n")

    sample_parameters = {
        "sampleSize" : sampleSize,
        "contrast" : float(arguments.contrast),
        "contrastbreak" : int(arguments.contrastbreak),
        "blur" : int(arguments.blur)**3,
    }

    output_parameters = {
        "characters" : characters,
        "outputFile" : arguments.output, #None or string
        "hide" : arguments.hide, #bool
        "foreground" : arguments.foreground, #bool
        "background" : arguments.background #bool or string with color code
    }

    return sample_parameters, palette, output_parameters

#TODO make filters to filter noise colors
def sample(imgpx,xa,ya,sampleSize,contrast,contrastbreak,blur,palette):
    #sampling
    if palette.muteable:
        palette=colorUtils.ColorPalette()
    else:
        palette.ground()
    for x in range(xa,xa+sampleSize[0]):
        for y in range(ya,ya+sampleSize[1]):
            if x<size[0] and y<size[1]:
                newPoint=colorUtils.ColorPoint(imgpx[x,y])
                #contrast
                newPoint.setContrast(contrast,contrastbreak)
                #main code
                if not(palette.muteable):
                    closestPoint, _ = find_closest_colorPoint(palette, newPoint)
                    closestPoint.weight+=1
                else:
                    closestPoint, d = find_closest_colorPoint(palette, newPoint)
                    if closestPoint==None:
                        palette.addpoint(newPoint)
                    elif d<((blur+closestPoint.weight)*0.24)**(1/3): #the weight of apoint increases the volume
                            closestPoint.r=(closestPoint.r*closestPoint.weight+newPoint.r)//(closestPoint.weight+1)
                            closestPoint.g=(closestPoint.g*closestPoint.weight+newPoint.g)//(closestPoint.weight+1)
                            closestPoint.b=(closestPoint.b*closestPoint.weight+newPoint.b)//(closestPoint.weight+1)
                            closestPoint.weight+=1
                    else:
                        palette.addpoint(newPoint)

    return find_greatest_2_colors(palette.colorPoints)

def find_greatest_2_colors(colorPoints):
    maxI=len(colorPoints)-1
    secondMaxI=0
    for i in range(len(colorPoints)):
        if colorPoints[maxI].weight<colorPoints[i].weight:
            secondMaxI=maxI
            maxI=i
        elif colorPoints[secondMaxI].weight<colorPoints[i].weight:
            secondMaxI=i
    return colorPoints[maxI], colorPoints[secondMaxI]

def calculate_distance(point0,point1):
    d=0
    d+=abs(point0.r-point1.r)**2
    d+=abs(point0.g-point1.g)**2
    d+=abs(point0.b-point1.b)**2
    return d**0.5

def find_closest_colorPoint(palette,targetPoint):
    """uses axis data structures in ColorPalette to quickly find closest point
    
    #< palette = ColorPalette
    #< targetPoint = ColorPoint

    #> closestPoint, distance

    After choosing a random point as the "closest so far"
    The furthest a potential closer point could be is directly on a cordinal line less then the distance you already got.
    """
    rpi=palette.search(palette.Raxis,targetPoint.r,key=lambda o: o.r)
    rmi=rpi-1
    gpi=palette.search(palette.Raxis,targetPoint.g,key=lambda o: o.g)
    gmi=gpi-1
    bpi=palette.search(palette.Raxis,targetPoint.b,key=lambda o: o.b)
    bmi=bpi-1
    min_d=800
    closestPoint=None
    n=1
    while n>0:
        n=0 #detect if any changes occured
        if rpi>-1 and rpi<len(palette.Raxis):
            if abs(palette.Raxis[rpi].r-targetPoint.r)<min_d:
                n+=1
                new_d=calculate_distance(palette.Raxis[rpi],targetPoint)
                if new_d<min_d:
                    min_d=new_d
                    closestPoint=palette.Raxis[rpi]
                    rpi=-1
                else:
                    rpi+=1
            else: rpi=-1
        if rmi>-1 and rmi<len(palette.Raxis):
            if abs(palette.Raxis[rmi].r-targetPoint.r)<min_d:
                n+=1
                new_d=calculate_distance(palette.Raxis[rmi],targetPoint)
                if new_d<min_d:
                    min_d=new_d
                    closestPoint=palette.Raxis[rmi]
                    rmi=-1
                else:
                    rmi-=1
            else: rmi=-1
        if gpi>-1 and gpi<len(palette.Gaxis): 
            if abs(palette.Gaxis[gpi].g-targetPoint.g)<min_d:
                n+=1
                new_d=calculate_distance(palette.Gaxis[gpi],targetPoint)
                if new_d<min_d:
                    min_d=new_d
                    closestPoint=palette.Gaxis[gpi]
                    gpi=-1
                else:
                    gpi+=1
            else: gpi=-1
        if gmi>-1 and gmi<len(palette.Gaxis):
            if abs(palette.Gaxis[gmi].g-targetPoint.g)<min_d:
                n+=1
                new_d=calculate_distance(palette.Gaxis[gmi],targetPoint)
                if new_d<min_d:
                    min_d=new_d
                    closestPoint=palette.Gaxis[gmi]
                    gmi=-1
                else:
                    gmi-=1
            else: gmi=-1
        if bpi>-1 and bpi<len(palette.Baxis): 
            if abs(palette.Baxis[bpi].b-targetPoint.b)<min_d:
                n+=1
                new_d=calculate_distance(palette.Baxis[bpi],targetPoint)
                if new_d<min_d:
                    min_d=new_d
                    closestPoint=palette.Baxis[bpi]
                    bpi=-1
                else:
                    bpi+=1
            else: bpi=-1
        if bmi>-1 and bmi<len(palette.Baxis):
            if abs(palette.Baxis[bmi].b-targetPoint.b)<min_d:
                n+=1
                new_d=calculate_distance(palette.Baxis[bmi],targetPoint)
                if new_d<min_d:
                    min_d=new_d
                    closestPoint=palette.Baxis[bmi]
                    bmi=-1
                else:
                    bmi+=1
            lse: bmi=-1
    return closestPoint, min_d
                
if __name__ == "__main__":
    #pre loading/parsing arguments and configs
    with open("config.yaml","r") as f:
        config=yaml.safe_load(f)
    arguments=cliparser.parse(config["Arguments"])

    debug_InfoMenager=debugInfoUtils.DebugInfoManager()
    debug_InfoMenager.stampStartTime()

    img = Image.open(arguments.filename)
    imgpx = img.load()
    size=img.size

    sample_parameters, palette, output_parameters = parseParameters(arguments)

    output_Manager=outputUtils.OutputManager(output_parameters)

    if output_parameters["hide"]:
        if output_parameters["outputFile"]==None:
            print("No output file specified. use `-o` for output.txt or `-o <filename>` for custom output file")
            exit()

    #doing the conversion
    debug_InfoMenager.printImageSize(size)
    debug_InfoMenager.printNewImageSize(size,sample_parameters["sampleSize"])

    defualt_line=""

    if type(background)==str:
        if not(hide):
            default_line=palette.monopattern.format(color=background,ESC="\033")

    for ya in range(0,size[1],sample_parameters["sampleSize"][1]):
        #TODO rewrite line to be a list
        line=defualt_line
        for xa in range(0,size[0],sample_parameters["sampleSize"][0]):
            color0, color1=sample(imgpx,xa,ya,**sample_parameters,palette=palette)
            line+=outputUtils.generatePixel(palette, color0, color1,  output_parameters, sample_parameters["sampleSize"])
        line+="\n"
        if outputFile!=None:
            outputContent.append(line)
    #complex printing stuff
        if not(hide):
            print(line,end="\033[0m")
        #if the output is hidden -> show percentages
        else:
            print(f"\r{str(round((ya/size[1])*100,1))}%",end="")
    if hide:
        print("\rDone   ")

    #save output to file
    if outputFile!=None:
        if not('.' in outputFile):
            outputFile+='.txt'
        with open(outputFile,"w") as f:
            for line in outputContent:
                f.write(line)
        print("Saved output to\033[1m",outputFile,"\033[0m")

    debug_InfoMenager.stampEndTime()
    debug_InfoMenager.printRunTIme()
