class OutputManager:
    def __init__(self,arguments,monopattern):
        self.passArguments(arguments)
        self.validateArguments()

        if self.outputFile!=None:
            self.output_Content=[]

        if type(self.background)==str:
            if self.outputFile!=None:
                self.output_Content.append(monopattern.format(color="48;2;"+self.background,ESC="\033"))

    def passArguments(self,arguments):
        self.outputFile = arguments["output_filename"] #None or string
        self.hide = arguments["hide"] #bool
        self.foreground = arguments["foreground"] #bool
        self.background = arguments["background"] #bool or string with color code
        self.characters = arguments["characters"] #str
        self.image_size = arguments["image_size"] #tuple
        self.sample_size = arguments["sample_size"]
    
    def validateArguments(self):
        if self.hide:
            if self.outputFile==None:
                print("No output file specified. use `-o` for output.txt or `-o <filename>` for custom output file")
                exit()
        if self.foreground==False and self.background==False:
            print("You can't have both no foreground and no background. (it's pointless)")
            exit()

    def addPixel(self,palette):
        pixel=self._generatePixel(palette)
        if not(self.hide):
            print(pixel,end="")
        if self.outputFile!=None:
            self.output_Content.append(pixel)

    def startLine(self,monopattern): #TODO maybe figure out a better way to pass monopattern
        if not(self.hide) and type(self.background)==str:
            print(monopattern.format(color="48;2;"+self.background,ESC="\033"),end="")

    def endLine(self,lineN):
        if not(self.hide):
            print()
        #if the output is hidden -> show percentages
        else:
            print(f"\r{str(round((lineN/self.image_size[1])*100,1))}%",end="")
        if self.outputFile!=None:
            self.output_Content.append("\n")

    def createOutputFile(self):
        if self.hide: #replace the percentage message from .addNewLine()
            print("\rDone   ")
        if self.outputFile!=None:
            #TODO rework this part about filename extension checks
            #TODO validate (check if perhaps repeating filename)
            if not('.' in self.outputFile):
                self.outputFile+='.txt'
            with open(self.outputFile,"w") as f:
                for item in self.output_Content:
                    f.write(item)
            print("\033[0mSaved output to\033[1m",self.outputFile,"\033[0m")

    def _generatePixel(self,palette):
            #TODO this could be optimized and will have to be adjusted once filters are implemented
            palette.colorPoints.sort(key=lambda colorPoint: colorPoint.weight, reverse=True)
            color0=palette.colorPoints[0]
            color1=palette.colorPoints[1]

            pixel=""
            fraction_0=color0.weight/(color0.weight+color1.weight)
            fraction_1=1-fraction_0

            #TODO fix pattern formatting and this mess
            if self.foreground==True and self.background==True:
                pixel+=palette.duopattern.format(ESC="\033",foreground=palette.foreground_prefix+color1.getForeground(),background=palette.background_prefix+color0.getBackground())
                pixel+=self.characters[round(fraction_1*2*(len(self.characters)-1))]
            elif self.foreground==True:
                fraction_from_sample=color0.weight/(self.sample_size[0]*self.sample_size[1])
                pixel+=palette.monopattern.format(ESC="\033",color=palette.foreground_prefix+color0.getForeground())
                pixel+=self.characters[round((fraction_from_sample-0.5)*2*(len(self.characters)-1))]
            elif self.background==True:
                pixel+=palette.monopattern.format(ESC="\033",color=palette.background_prefix+color0.getBackground())
                pixel+=" "
            return pixel
