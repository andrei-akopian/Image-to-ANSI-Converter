import json

def loadPalette(palettename):
    palette=ColorPalette()
    #if custom palette provided -> load it
    if palettename!=None:
        #open file
        if not("/" in palettename):
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

        # * NOTE: the colorPoints will NOT remain in order
        for cp in data["colors"]:
            palette.addpoint(ColorPoint(cp[2]))
            palette.colorPoints[-1].foreground=cp[0]
            palette.colorPoints[-1].background=cp[1]
    return palette

class ColorPalette:
    def __init__(self):
        self.monopattern="{ESC}[{color}m"
        self.duopattern="{ESC}[{foreground}m{ESC}[{background}m"
        self.colorPoints=[]
        self.Raxis=[]
        self.Gaxis=[]
        self.Baxis=[]
        self.muteable=True
        self.foreground_prefix="38;2;"
        self.background_prefix="48;2;"

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
        for point in self.colorPoints:
            point.weight=1

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

    # * using native .sort is actually faster
    # def find_greatest_2_colors(colorPoints):
    #     maxI=len(colorPoints)-1
    #     secondMaxI=0
    #     for i in range(len(colorPoints)):
    #         if colorPoints[maxI].weight<colorPoints[i].weight:
    #             secondMaxI=maxI
    #             maxI=i
    #         elif colorPoints[secondMaxI].weight<colorPoints[i].weight:
    #             secondMaxI=i
    #     return colorPoints[maxI], colorPoints[secondMaxI]

class ColorPoint:
    def __init__(self,color):
        self.r=color[0]
        self.g=color[1]
        self.b=color[2]
        self.weight=1
        self.foreground=""
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
