
"""
Read, load, cli, configs and other inputs
"""

import argparse
import yaml
import os
from PIL import Image
import math

def getYamlFile(filepath):
    with open(filepath,"r") as f:
        return yaml.safe_load(f)

#TODO fix this. Make all default arguments come from argumentfile. Tracking defaults from user inputs is impossible
def getInput():
    argparseArguments=getYamlFile("utils/argparseArguments.yaml")
    raw_arguments=parsecli(argparseArguments["Arguments"])
    if raw_arguments.argumentfile!=None: #TODO make it so that custom inputs overwrite fileinput
        arguments=getYamlFile(raw_arguments.argumentfile)
    else:
        arguments=processInputs(raw_arguments) #dictionary
    return arguments

def overwriteDefaultArguments(arguments,raw_arguments,argparseArguments):
    return arguments

def parsecli(ArgsParserArguments):
    parser=argparse.ArgumentParser(
        prog="Image to ANSI converter"
    )

    parser.add_argument("-af","--argumentfile",default=ArgsParserArguments["argumentfile"]["default"],help=ArgsParserArguments["argumentfile"]["help"])

    parser.add_argument("-f","--filename",default=ArgsParserArguments["filename"]["default"],help=ArgsParserArguments["filename"]["help"])
    parser.add_argument("-o","--output",nargs='?',default=ArgsParserArguments["output"]["default"],const=ArgsParserArguments["output"]["const"],help=ArgsParserArguments["output"]["help"])

    parser.add_argument("-c","--contrast",default=ArgsParserArguments["contrast"]["default"],help=ArgsParserArguments["contrast"]["help"])
    parser.add_argument("-cb","--contrastbreak",default=ArgsParserArguments["contrastbreak"]["default"],help=ArgsParserArguments["contrastbreak"]["help"])
    parser.add_argument("-s","--sample_size",default=ArgsParserArguments["sample_size"]["default"],help=ArgsParserArguments["sample_size"]["help"])
    parser.add_argument("-os","--output_size",default=ArgsParserArguments["output_size"]["default"],help=ArgsParserArguments["output_size"]["help"])
    parser.add_argument("-b","--blur",default=ArgsParserArguments["blur"]["default"],help=ArgsParserArguments["blur"]["help"])

    parser.add_argument("--hide", action='store_const',const=True, default=ArgsParserArguments["hide"]["default"], help=ArgsParserArguments["hide"]["help"])
    parser.add_argument("-p","--palettename",default=ArgsParserArguments["palettename"]["default"],help=ArgsParserArguments["palettename"]["help"])
    parser.add_argument("-fp","--filterpalettename",default=ArgsParserArguments["filterpalettename"]["default"],help=ArgsParserArguments["filterpalettename"]["help"])
    parser.add_argument("-char","--characters", default=ArgsParserArguments["characters"]["default"], help=ArgsParserArguments["characters"]["help"])
    parser.add_argument("-charf","--characterfile", default=ArgsParserArguments["characterfile"]["default"], help=ArgsParserArguments["characterfile"]["help"])
    parser.add_argument("-nfg","--noforeground",action='store_const',const=False, dest="foreground", default=ArgsParserArguments["background"]["default"], help=ArgsParserArguments["background"]["help"])
    parser.add_argument("-nbg","--nobackground",nargs='?',const=False,default=ArgsParserArguments["foreground"]["default"], dest="background", help=ArgsParserArguments["foreground"]["help"])

    return parser.parse_args()

def processInputs(raw_arguments):
    #TODO many values need validation (add vlidation in the appropriate places) (value range validation)
    arguments={
        "argumentfile":raw_arguments.argumentfile,

        "image_filename":raw_arguments.filename,
        "output_filename":raw_arguments.output,

        "contrast":int(raw_arguments.contrast),
        "contrastbreak":int(raw_arguments.contrastbreak),
        "sample_size":processSampleSize(raw_arguments.sample_size), #tuple [w,h],
        "output_size":raw_arguments.output_size, #tuple [w,h]
        "blur":int(raw_arguments.blur),
        "image_size":[0,0], #modified after image is parsed

        "hide":raw_arguments.hide,
        "palettename":raw_arguments.palettename,
        "filterpalettename":raw_arguments.filterpalettename,
        "characters":processCharacters(raw_arguments.characters,raw_arguments.characterfile), #str
        "foreground":raw_arguments.foreground,
        "background":raw_arguments.background
    }
    return arguments

def processSampleSize(raw_sample_size):
    if "x" in raw_sample_size:
        sample_size=list(map(int,raw_sample_size.split("x")))
    else:
        int_sample_size=int(raw_sample_size)
        sample_size=[int_sample_size,int_sample_size]
    return sample_size

def processCharacters(raw_characters,raw_characterfile): 
    #< [str, None or str] 
    #> str
    if raw_characterfile!=None:
        with open(raw_characterfile,"r") as f:
            characters=f.read().strip("\n")
        return characters
    else:
        return raw_characters

def processOutputSize(image_size,output_size,sample_size):
    """
    #< image_size = (w,h)
    #< output_size = (w,h) or "WxH"

    #> sample_size = [w,h]
    """
    if output_size!=None:
        if output_size==str: #* It could also be a list
            try:
                output_size=list(map(int,output_size.split("x")))
                if len(output_size)!=2:
                    raise Exception(f"\033[1m Incorrect --output_size input. Specify as WxH eg. 20x20")
            except:
                raise Exception(f"\033[1m Bad --output_size input. Specify as WxH eg. 20x20")
        sample_size[0],sample_size[1]=math.ceil(image_size[0]/output_size[0]),math.ceil(image_size[1]/output_size[1])

    return sample_size

def getImage(image_filename):
    if not os.path.exists(image_filename):
        raise ValueError(f"\033[1m'{image_filename}' does not exist")
    if not os.path.isfile(image_filename):
        raise ValueError(f"\033[1m'{image_filename}' is not a file")
    try: #TODO potentially add correct filename suggestion
        img = Image.open(image_filename)
    except:
        raise ValueError(f"\033[1m'{image_filename}' is not an image file")
    else:
        return img