class OutputManager:
    def __init__(self,arguments):
        self.passArguments(arguments)
        self.validateArguments()
        if self.outputFile!=None:
            self.output_Content=[]
        if type(self.background)==str:
            if self.outputFile!=None:
                self.output_Content.append(palette.monopattern.format(color=self.background,ESC="\033"))

    def passArguments(self,arguments):
        self.outputFile = arguments["outputFile"], #None or string
        self.hide = arguments["hide"] #bool
        self.foreground = arguments["foreground"] #bool
        self.background = arguments["background"] #bool or string with color code
        self.characters = arguments["characters"] #str
        self.image_size = arguments["image_size"] #tuple
    
    def validateArguments(self):
        if self.hide:
            if self.outputFile==None:
                print("No output file specified. use `-o` for output.txt or `-o <filename>` for custom output file")
                exit()

    def addPixel(self,palette):
        pass

    def addNewLine(self):
        print("\n")
        if self.outputFile!=None:
            self.output_Content.append("\n")

    def addWriteOutput(self):
        #TODO validate (check if perhaps repeating filename)
        pass



def generatePixel(palette,color0,color1,sampleSize):
        pixel=""
        fraction_0=color0.weight/(color0.weight+color1.weight)
        fraction_1=1-fraction_0

        #FIXME add a way to pass these as arguments
        foreground = output_parameters["foreground"]
        background = output_parameters["background"]
        characters = output_parameters["characters"]
        
        #FIXME fix pattern formatting and this mess
        if foreground==True and background==True:
            pixel+=palette.duopattern.format(ESC="\033",foreground=palette.foreground_prefix+color1.getForeground(),background=palette.background_prefix+color0.getBackground())
            pixel+=characters[round(fraction_1*2*(len(characters)-1))]
        elif foreground==True:
            fraction_from_sample=color0.weight/(sampleSize[0]*sampleSize[1])
            pixel+=palette.monopattern.format(ESC="\033",color=palette.foreground_prefix+color0.getForeground())
            pixel+=characters[round((fraction_from_sample-0.5)*2*(len(characters)-1))]
        elif background:
            pixel+=palette.monopattern.format(ESC="\033",color=palette.background_prefix+color0.getBackground())
            pixel+=" "
        else:
            pixel+=" "
        return pixel
