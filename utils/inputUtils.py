
"""
Read, load, cli, configs and other inputs
"""

import argparse
import yaml

def getConfigFile(filepath="config.yaml"):
    with open(filepath,"r") as f:
        return yaml.safe_load(f)

def getInput(config):
    raw_arguments=parsecli(config["Arguments"])
    arguments=processInputs(raw_arguments) #dictionary
    return arguments

def parsecli(ArgsParserArguments): #TODO rewrite it so that all the parameters can be specified in yaml
    parser=argparse.ArgumentParser(
        prog="Image to ANSI converter"
    )

    parser.add_argument("-f","--filename",default=ArgsParserArguments["filename"]["default"],help=ArgsParserArguments["filename"]["help"])
    parser.add_argument("-o","--output",nargs='?',default=ArgsParserArguments["output"]["default"],const=ArgsParserArguments["output"]["const"],help=ArgsParserArguments["output"]["help"])

    parser.add_argument("-c","--contrast",default=ArgsParserArguments["contrast"]["default"],help=ArgsParserArguments["contrast"]["help"])
    parser.add_argument("-cb","--contrastbreak",default=ArgsParserArguments["contrastbreak"]["default"],help=ArgsParserArguments["contrastbreak"]["help"])
    parser.add_argument("-s","--sampleSize",default=ArgsParserArguments["sampleSize"]["default"],help=ArgsParserArguments["sampleSize"]["help"])
    parser.add_argument("-b","--blur",default=ArgsParserArguments["blur"]["default"],help=ArgsParserArguments["blur"]["help"])

    parser.add_argument("--hide", action='store_const',const=True, default=ArgsParserArguments["hide"]["default"], help=ArgsParserArguments["hide"]["help"])
    parser.add_argument("-p","--palettename",default=ArgsParserArguments["palettename"]["default"],help=ArgsParserArguments["palettename"]["help"])
    parser.add_argument("-char","--characters", default=ArgsParserArguments["characters"]["default"], help=ArgsParserArguments["characters"]["help"])
    parser.add_argument("-charf","--characterfile", default=ArgsParserArguments["characterfile"]["default"], help=ArgsParserArguments["characterfile"]["help"])
    parser.add_argument("-nfg","--noforeground",action='store_const',const=False, dest="foreground", default=ArgsParserArguments["background"]["default"], help=ArgsParserArguments["background"]["help"])
    parser.add_argument("-nbg","--nobackground",nargs='?',const=False,default=ArgsParserArguments["foreground"]["default"], dest="background", help=ArgsParserArguments["foreground"]["help"])

    return parser.parse_args()

def processInputs(raw_arguments):
    #TODO many values need validation (add vlidation in the appropriate places) (value range validation)
    arguments={
        "image_filename":raw_arguments.filename,
        "output_filename":raw_arguments.output,

        "contrast":int(raw_arguments.contrast),
        "contrastbreak":int(raw_arguments.contrastbreak),
        "sample_size":processSampleSize(raw_arguments.sampleSize), #tuple [w,h]
        "blur":int(raw_arguments.blur),
        "image_size":[0,0], #modified after image is parsed

        "hide":raw_arguments.hide,
        "palettename":raw_arguments.palettename,
        "characters":processCharacters(raw_arguments.characters,raw_arguments.characterfile), #str
        "foreground":raw_arguments.foreground,
        "background":raw_arguments.background
    }
    return arguments

def processSampleSize(raw_sampleSize):
    if "x" in raw_sampleSize:
        sampleSize=list(map(int,raw_sampleSize.split("x")))
    else:
        int_sampleSize=int(raw_sampleSize)
        sampleSize=[int_sampleSize,int_sampleSize]
    return sampleSize

def processCharacters(raw_characters,raw_characterfile): 
    #< [str, None or str] 
    #> str
    if raw_characterfile!=None:
        with open(raw_characterfile,"r") as f:
            characters=f.read().strip("\n")
        return characters
    else:
        return raw_characters