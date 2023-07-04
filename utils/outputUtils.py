import os

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
                raise Exception("\033[1mNo output file specified. use `-o` for output.txt or `-o <filename>` for custom output file")
        if self.foreground==False and self.background==False:
            raise Exception("\033[1mYou can't have both no foreground and no background. (it's pointless)")
        #validate output filename
        if self.outputFile!=None:
            while os.path.exists(self.outputFile): #TODO add an option to override from the clargs
                path, file_extension = os.path.splitext(self.outputFile)
                print(f"\033[1mWarning\033[0m: File {self.outputFile} already exists")
                print(f"Press 'Enter' to overwrite or enter '+' to rename into {path}_1{file_extension}")
                new_filename=input("or enter new filename: ")
                if new_filename=="":
                    break
                elif new_filename=="+": #TODO make it incrament filename count if similar filename already exists
                    self.outputFile=path+"_1"+file_extension
                else:
                    self.outputFile=new_filename

    def addPixel(self,palette):
        palette.findMax2()
        pixel=self._findAnsiColorCode(palette)
        pixel+=self._findCharacter(palette)
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
        if self.hide: #replaces the percentage message from .addNewLine()
            print("\rDone   ")
        if self.outputFile!=None:
            with open(self.outputFile,"w") as f:
                for item in self.output_Content:
                    f.write(item)
            print(f"\033[0mSaved {os.path.getsize(self.outputFile)} bytes to\033[1m {self.outputFile}\033[0m")

    def _findAnsiColorCode(self,palette):
            ansi_color_code=""

            if self.foreground==True and self.background==True:
                ansi_color_code=palette.duopattern.format(ESC="\033",foreground=palette.foreground_prefix+palette.color1.getForeground(),background=palette.background_prefix+palette.color0.getBackground())
            elif self.foreground==True:
                ansi_color_code=palette.monopattern.format(ESC="\033",color=palette.foreground_prefix+palette.color0.getForeground())
            elif self.background==True:
                ansi_color_code=palette.monopattern.format(ESC="\033",color=palette.background_prefix+palette.color0.getBackground())
            return ansi_color_code

    def _findCharacter(self,palette):
        character=""
        if self.foreground==True and self.background==True:
            fraction_0=palette.color0.weight/(palette.color0.weight+palette.color1.weight)
            fraction_1=1-fraction_0
            character=self.characters[round(fraction_1*2*(len(self.characters)-1))]
        elif self.foreground==True:
            fraction_from_sample=palette.color0.weight/(self.sample_size[0]*self.sample_size[1])
            character=self.characters[round((fraction_from_sample-0.5)*2*(len(self.characters)-1))]
        elif self.background==True:
            character=" "
        return character

