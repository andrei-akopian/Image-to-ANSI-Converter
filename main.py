from utils import colorUtils, inputUtils, outputUtils, debugInfoUtils

def convertImage(imgpx, palette, arguments, output_Manager, debug_InfoMenager, adjusted_functions):
    debug_InfoMenager.stampStartTime()

    ## doing the conversion
    # print image sizes
    debug_InfoMenager.printImageSize(arguments["image_size"])
    debug_InfoMenager.printNewImageSize(arguments["image_size"],arguments["sample_size"])

    for ya in range(0,arguments["image_size"][1]//arguments["sample_size"][1]):
        ya=ya*arguments["sample_size"][1]
        output_Manager.startLine(palette.monopattern)

        for xa in range(0,arguments["image_size"][0]//arguments["sample_size"][0]):
            xa=xa*arguments["sample_size"][0]
            palette=sample(imgpx,xa,ya,palette,arguments,adjusted_functions)
            output_Manager.addPixel(palette)
        #FIXME last column is cut off if sample_size doesn't match it completely (done to make output_size feature work)
        #make this a custom option

        if arguments["use_debug"]:
            if arguments["debug"]["stamp_interval_times"]:
                debug_InfoMenager.stampInterval()
                debug_InfoMenager.printLastInterval()

        output_Manager.endLine(ya)

    output_Manager.createOutputFile()

    debug_InfoMenager.stampEndTime()
    debug_InfoMenager.printRunTime()

def sample(imgpx,xa,ya,palette,arguments,adjusted_functions):
    #sampling
    palette.ground()
    for x in range(xa,xa+arguments["sample_size"][0]):
        for y in range(ya,ya+arguments["sample_size"][1]):
            if x<arguments["image_size"][0] and y<arguments["image_size"][1]:
                newPoint=colorUtils.ColorPoint(imgpx[x,y])
                #contrast
                newPoint.setContrast(arguments["contrast"],arguments["contrastbreak"])
                #figuring out what that point does to the statistics
                closestPoint, d = adjusted_functions["findClosestColorPoint"](palette, newPoint, adjusted_functions["calculateDistance"])
                if not(palette.muteable):
                    closestPoint.weight+=1
                else:
                    if closestPoint==None:
                        palette.appendPoint(newPoint)
                        if arguments["convert_image"]["algorithm_specifications"]["find_closest_color_point_algorithm"] == "a":
                            palette.addPointToAxies(newPoint)
                    elif not(closestPoint.muteable): #TODO make filter less effective/add control for the effectiveness
                        closestPoint.weight+=1 #TODO maybe I should make filterPoints adjust their color
                    elif d<((arguments["blur"]+closestPoint.weight)*0.24)**(1/3): #the weight of a point increases it's the volume
                        closestPoint.r=(closestPoint.r*closestPoint.weight+newPoint.r)//(closestPoint.weight+1)
                        closestPoint.g=(closestPoint.g*closestPoint.weight+newPoint.g)//(closestPoint.weight+1)
                        closestPoint.b=(closestPoint.b*closestPoint.weight+newPoint.b)//(closestPoint.weight+1)
                        closestPoint.weight+=1
                    else:
                        palette.appendPoint(newPoint)
                        if arguments["convert_image"]["algorithm_specifications"]["find_closest_color_point_algorithm"] == "a":
                            palette.addPointToAxies(newPoint)
    return palette

def setAdjustedFunctions(arguments):
    def calculate_pythagorean_distance(point0,point1):
        d=0
        d+=abs(point0.r-point1.r)**2
        d+=abs(point0.g-point1.g)**2
        d+=abs(point0.b-point1.b)**2
        d=d**0.5
        return d, d/1.7321 #d/sqrt(3)

    def calculate_manhattan_distance(point0,point1):
        d=0
        d+=abs(point0.r-point1.r)
        d+=abs(point0.g-point1.g)
        d+=abs(point0.b-point1.b)
        return d, d/3

    def findClosestColorPointAndvanced(palette,targetPoint,calculateDistance):
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
        check_d=800 #how far to check
        closestPoint=None
        n=1
        while n>0:
            n=0 #detect if any changes occured
            if rpi>-1 and rpi<len(palette.Raxis):
                if abs(palette.Raxis[rpi].r-targetPoint.r)<check_d:
                    n+=1
                    new_d, new_check_d=calculateDistance(palette.Raxis[rpi],targetPoint)
                    if new_d<min_d:
                        min_d=new_d
                        check_d=new_check_d
                        closestPoint=palette.Raxis[rpi]
                        rpi=-1
                    else:
                        rpi+=1
                else: 
                    rpi=-1
            if rmi>-1 and rmi<len(palette.Raxis):
                if abs(palette.Raxis[rmi].r-targetPoint.r)<check_d:
                    n+=1
                    new_d, new_check_d=calculateDistance(palette.Raxis[rmi],targetPoint)
                    if new_d<min_d:
                        min_d=new_d
                        check_d=new_check_d
                        closestPoint=palette.Raxis[rmi]
                        rmi=-1
                    else:
                        rmi-=1
                else: 
                    rmi=-1
            if gpi>-1 and gpi<len(palette.Gaxis): 
                if abs(palette.Gaxis[gpi].g-targetPoint.g)<check_d:
                    n+=1
                    new_d, new_check_d=calculateDistance(palette.Gaxis[gpi],targetPoint)
                    if new_d<min_d:
                        min_d=new_d
                        check_d=new_check_d
                        closestPoint=palette.Gaxis[gpi]
                        gpi=-1
                    else:
                        gpi+=1
                else: 
                    gpi=-1
            if gmi>-1 and gmi<len(palette.Gaxis):
                if abs(palette.Gaxis[gmi].g-targetPoint.g)<check_d:
                    n+=1
                    new_d, new_check_d=calculateDistance(palette.Gaxis[gmi],targetPoint)
                    if new_d<min_d:
                        min_d=new_d
                        check_d=new_check_d
                        closestPoint=palette.Gaxis[gmi]
                        gmi=-1
                    else:
                        gmi-=1
                else: 
                    gmi=-1
            if bpi>-1 and bpi<len(palette.Baxis): 
                if abs(palette.Baxis[bpi].b-targetPoint.b)<check_d:
                    n+=1
                    new_d, new_check_d=calculateDistance(palette.Baxis[bpi],targetPoint)
                    if new_d<min_d:
                        min_d=new_d
                        check_d=new_check_d
                        closestPoint=palette.Baxis[bpi]
                        bpi=-1
                    else:
                        bpi+=1
                else: 
                    bpi=-1
            if bmi>-1 and bmi<len(palette.Baxis):
                if abs(palette.Baxis[bmi].b-targetPoint.b)<check_d:
                    n+=1
                    new_d, new_check_d=calculateDistance(palette.Baxis[bmi],targetPoint)
                    if new_d<min_d:
                        min_d=new_d
                        check_d=new_check_d
                        closestPoint=palette.Baxis[bmi]
                        bmi=-1
                    else:
                        bmi-=1
                else: 
                    bmi=-1
        return closestPoint, min_d

    def findClosestColorPointBrute(palette,targetPoint,calculateDistance):
        min_d=800
        closestPoint=None
        for colorPoint in palette.colorPoints:
            new_d, _ =calculateDistance(colorPoint,targetPoint)
            if new_d<min_d:
                min_d=new_d
                closestPoint=colorPoint
        return closestPoint, min_d

    def setDistanceCalculationAlgorithm(distance_calculation_algorithm):
        if distance_calculation_algorithm == "m":
            calculate_distance=calculate_manhattan_distance
        elif distance_calculation_algorithm == "p":
            calculate_distance=calculate_pythagorean_distance
        else:
            raise Exception("\033[1mIncorrect distance calculation algorithm specification")
        return calculate_distance

    def setClosestColorPointAlgorithm(find_closest_color_point_algorithm):
        if find_closest_color_point_algorithm == "a":
            findClosestColorPoint=findClosestColorPointAndvanced
        elif find_closest_color_point_algorithm == "b":
            findClosestColorPoint=findClosestColorPointBrute
        else:
            raise Exception("\033[1mIncorrect find closest color point algorithm specification")
        return findClosestColorPoint

    adjusted_functions={}
    adjusted_functions["calculateDistance"] = setDistanceCalculationAlgorithm(arguments["distance_calculation_algorithm"])  
    adjusted_functions["findClosestColorPoint"] = setClosestColorPointAlgorithm(arguments["find_closest_color_point_algorithm"])
    return adjusted_functions

def perperation(arguments):
    debug_InfoMenager=debugInfoUtils.DebugInfoManager(arguments["hide"])

    #create/load palette:
    palette=colorUtils.loadPalette(arguments["palettename"])
    if arguments["filterpalettename"]!=None:
        colorUtils.loadFilter(arguments["filterpalettename"],palette)

    #algorithm specifications
    adjusted_functions = setAdjustedFunctions(arguments["convert_image"]["algorithm_specifications"])
    
    output_Manager=outputUtils.OutputManager(arguments,palette.monopattern)

    return palette, arguments, output_Manager, debug_InfoMenager, adjusted_functions

if __name__ == "__main__":
    #parse arguments
    arguments, imgpx=inputUtils.getInput()

    convertImage(imgpx,*perperation(arguments))