class OutputManager:
    def __init__(self,output_parameters):
        pass

def generatePixel(palette,color0,color1,output_parameters,sampleSize):
        pixel=""
        fraction_0=color0.weight/(color0.weight+color1.weight)
        fraction_1=1-fraction_0

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