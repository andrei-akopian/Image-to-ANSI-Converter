from PIL import Image
from utils import colorUtils, inputUtils, outputUtils, debugInfoUtils

def sample(imgpx,xa,ya,palette,arguments):
    #sampling
    palette.ground()
    for x in range(xa,xa+arguments["sample_size"][0]):
        for y in range(ya,ya+arguments["sample_size"][1]):
            if x<arguments["image_size"][0] and y<arguments["image_size"][1]:
                newPoint=colorUtils.ColorPoint(imgpx[x,y])
                #contrast
                newPoint.setContrast(arguments["contrast"],arguments["contrastbreak"])
                #figuring out what that point does to the statistics
                closestPoint, d = find_closest_colorPoint(palette, newPoint)
                if not(palette.muteable):
                    closestPoint.weight+=1
                else:
                    if closestPoint==None:
                        palette.addpoint(newPoint)
                    elif closestPoint.is_filter:
                        closestPoint.weight+=1 # * maybe I should make fitlerPoints adjust their color
                    elif d<((arguments["blur"]+closestPoint.weight)*0.24)**(1/3): #the weight of a point increases it's the volume
                            closestPoint.r=(closestPoint.r*closestPoint.weight+newPoint.r)//(closestPoint.weight+1)
                            closestPoint.g=(closestPoint.g*closestPoint.weight+newPoint.g)//(closestPoint.weight+1)
                            closestPoint.b=(closestPoint.b*closestPoint.weight+newPoint.b)//(closestPoint.weight+1)
                            closestPoint.weight+=1
                    else:
                        palette.addpoint(newPoint)

    return palette

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

    The script finds the points rough position an the palette.[R,G,B]axis
    After choosing a nearby point as the "closest so far"
    The furthest a potential closer point could be is directly on a cordinal line less then the distance you already got.
    """
    rpi=palette.search(palette.Raxis,targetPoint.r,key=lambda o: o.r)
    rmi=rpi-1
    gpi=palette.search(palette.Raxis,targetPoint.g,key=lambda o: o.g)
    gmi=gpi-1
    bpi=palette.search(palette.Raxis,targetPoint.b,key=lambda o: o.b)
    bmi=bpi-1
    min_d=800 #255*3
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
    #parse arguments
    arguments=inputUtils.getInput()

    #load initiate debug_InfoMenager and stamp start time
    debug_InfoMenager=debugInfoUtils.DebugInfoManager(arguments["hide"])
    debug_InfoMenager.stampStartTime()

    #load image & put img.size into arguments
    img = Image.open(arguments["image_filename"]) #TODO validate (write a seperate function)
    imgpx = img.load()
    image_size=img.size
    arguments["image_size"] = image_size

    #create/load palette:
    palette=colorUtils.loadPalette(arguments["palettename"])
    if arguments["filterpalettename"]!=None:
        # print("Loading filterpalette:",arguments["filterpalettename"])
        colorUtils.loadFilter(arguments["filterpalettename"],palette)

    output_Manager=outputUtils.OutputManager(arguments,palette.monopattern)

    ## doing the conversion
    # print image sizes #TODO add runtime estimate
    debug_InfoMenager.printImageSize(image_size)
    debug_InfoMenager.printNewImageSize(image_size,arguments["sample_size"])

    for ya in range(0,image_size[1],arguments["sample_size"][1]):
        output_Manager.startLine(palette.monopattern)

        for xa in range(0,image_size[0],arguments["sample_size"][0]):
            palette=sample(imgpx,xa,ya,palette=palette,arguments=arguments)
            output_Manager.addPixel(palette)

        debug_InfoMenager.stampInterval()
        debug_InfoMenager.printLastInterval()

        output_Manager.endLine(ya)

    output_Manager.createOutputFile()

    debug_InfoMenager.stampEndTime()
    debug_InfoMenager.printRunTIme()
