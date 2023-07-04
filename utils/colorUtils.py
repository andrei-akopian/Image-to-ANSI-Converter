import json

def loadPalette(palettename):
    palette=ColorPalette()
    #if custom palette provided -> load it
    if palettename!=None:
        #open file
        if not("/" in palettename): #TODO add validation
            palettename="palettes/"+palettename+".json"
        data={}
        with open(palettename,"r") as f:
            data=json.load(f)
        #create palette
        palette.muteable=False
        palette.monopattern=data["monopattern"]
        palette.duopattern=data["duopattern"]
        palette.foreground_prefix=data["foreground_prefix"]
        palette.background_prefix=data["background_prefix"]

        for cp in data["colors"]:
            color_Point=ColorPoint(cp[2])
            color_Point.foreground=cp[0]
            color_Point.background=cp[1]
            palette.addpoint(color_Point)
    return palette

def loadFilter(filterpalettename,palette):
    #open file
    if not("/" in filterpalettename): #TODO add validation
        filterpalettename="palettes/"+filterpalettename+".json"
    data={}
    with open(filterpalettename,"r") as f:
        data=json.load(f)
    #add the filters to palette
    palette.with_filter=True
    for cp in data["colors"]: #TODO allow a simpler version of filter palettes
        color_Point=ColorPoint(cp[2])
        color_Point.is_filter=True
        palette.addpoint(color_Point)

class ColorPalette:
    def __init__(self):
        self.monopattern="{ESC}[{color}m"
        self.duopattern="{ESC}[{foreground}m{ESC}[{background}m"
        self.foreground_prefix="38;2;"
        self.background_prefix="48;2;"

        self.colorPoints=[]
        self.Raxis=[]
        self.Gaxis=[]
        self.Baxis=[]

        self.muteable=True
        self.with_filter=False

        #to store the max to colors .findMax2() from
        self.color0=None
        self.color1=None

    def addpoint(self,point):
        self.colorPoints.append(point)
        self.Raxis.insert(self.search(self.Raxis,point.r,key=lambda o: o.r),point)
        self.Gaxis.insert(self.search(self.Gaxis,point.g,key=lambda o: o.g),point)
        self.Baxis.insert(self.search(self.Baxis,point.b,key=lambda o: o.b),point)
    
    def search(self,axis,target,start=0,end=-1,key=lambda o: o.r): #TODO can be improved
        #< target is a numeral
        #binary search to locate the position a point is on the axies
        if end==-1:
            end=len(axis)
        if start==end:
            return start
        elif target>key(axis[(start+end)//2]):
            return self.search(axis,target,(start+end)//2+1,end,key)
        else:
            return self.search(axis,target,start,(start+end)//2,key)

    def ground(self):
        cpI=0
        self.color0=None
        self.color1=None
        if self.muteable and self.with_filter:
            while cpI < len(self.colorPoints):
                if self.colorPoints[cpI].is_filter:
                    self.colorPoints[cpI].weight=1
                    cpI+=1
                else:
                    self.Raxis.remove(self.colorPoints[cpI])
                    self.Gaxis.remove(self.colorPoints[cpI])
                    self.Baxis.remove(self.colorPoints[cpI])
                    del self.colorPoints[cpI]
        elif self.muteable and not(self.with_filter):
            del self.colorPoints[:]
            del self.Raxis[:]
            del self.Gaxis[:]
            del self.Baxis[:]
        elif not(self.muteable):
            while cpI < len(self.colorPoints):
                self.colorPoints[cpI].weight=1
                cpI+=1

    def fillPattern(self,fgcolor=None,bgcolor=None,ESC="\033"):
        #neighter
        if fgcolor==None and bgcolor==None:
            return ""
        #foreground only
        elif fgcolor==None:
            return self.monopattern.format(color=fgcolor,ESC=ESC)
        #background only
        elif bgcolor==None:
            return self.monopattern.format(color=bgcolor,ESC=ESC)
        else:
            return self.duopattern.format(foreground=fgcolor,background=bgcolor,ESC=ESC)

    def findMax2(self):
        maxI=None
        secondMaxI=None
        i=0
        while i<len(self.colorPoints):
            if not(self.colorPoints[i].is_filter):
                #maxI
                if maxI==None:
                    maxI=i
                elif self.colorPoints[maxI].weight<self.colorPoints[i].weight:
                    secondMaxI=maxI
                    maxI=i
                #secondMaxI
                elif secondMaxI==None:
                    secondMaxI=i
                elif self.colorPoints[secondMaxI].weight<self.colorPoints[i].weight:
                    secondMaxI=i
            i+=1
        if secondMaxI==None:
            secondMaxI=maxI
        if maxI==None:
            color_Point=ColorPoint([0,0,0])
            self.color0=color_Point
            self.color1=color_Point
        else:
            self.color0=self.colorPoints[maxI]
            self.color1=self.colorPoints[secondMaxI]
        return self.color0, self.color1

class ColorPoint:
    def __init__(self,color):
        self.r=color[0]
        self.g=color[1]
        self.b=color[2]
        self.weight=1
        self.foreground="" #TODO replace this with None
        self.background=""
        self.is_filter=0

    def getForeground(self):
        if self.foreground=="":
            return str(self.r)+";"+str(self.g)+";"+str(self.b)
        else:
            return self.foreground
    def getBackground(self):
        if self.background=="":
            return str(self.r)+";"+str(self.g)+";"+str(self.b)
        else:
            return self.background
    
    def setContrast(self,contrast,contrastbreak):
        if contrast!=1:
            if self.getBrightness()>contrastbreak:
                self.r=min(int(self.r*contrast),255)
                self.g=min(int(self.g*contrast),255)
                self.b=min(int(self.b*contrast),255)
            else:
                self.r=min(int(self.r/contrast),255)
                self.g=min(int(self.g/contrast),255)
                self.b=min(int(self.b/contrast),255)
            
    def getBrightness(self):
        self.brightness=0.33*self.r+0.5*self.g+0.16*self.b
        return self.brightness
