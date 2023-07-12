
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

def getInput():
    argparse_help_messages=getYamlFile("utils/argparseHelpMessages.yaml")
    raw_arguments=parsecli(argparse_help_messages)

    if raw_arguments["argumentfile"]!=None:
        arguments=getYamlFile(raw_arguments["argumentfile"])
    else:
        arguments=getYamlFile("utils/defaultargumentfile.yaml")
    arguments=processInputs(arguments,raw_arguments)

    return arguments

def parsecli(argparse_help_messages):
    parser=argparse.ArgumentParser(
        prog="Image to ANSI converter"
    )

    parser.add_argument("-af","--argumentfile",required=False,help=argparse_help_messages["argumentfile"]["help"])

    parser.add_argument("-f","--image_filename",required=False,help=argparse_help_messages["filename"]["help"])
    parser.add_argument("-o","--output_filename",nargs="?",required=False,const=argparse_help_messages["output"]["const"],help=argparse_help_messages["output"]["help"])

    parser.add_argument("-c","--contrast",required=False,help=argparse_help_messages["contrast"]["help"])
    parser.add_argument("-cb","--contrastbreak",required=False,help=argparse_help_messages["contrastbreak"]["help"])
    parser.add_argument("-s","--sample_size",required=False,help=argparse_help_messages["sample_size"]["help"])
    parser.add_argument("-os","--output_size",required=False,help=argparse_help_messages["output_size"]["help"])
    parser.add_argument("-b","--blur",required=False,help=argparse_help_messages["blur"]["help"])

    parser.add_argument("--hide", action='store_true', required=False, help=argparse_help_messages["hide"]["help"])
    parser.add_argument("-p","--palettename",required=False,help=argparse_help_messages["palettename"]["help"])
    parser.add_argument("-fp","--filterpalettename",required=False,help=argparse_help_messages["filterpalettename"]["help"])
    parser.add_argument("-char","--characters", required=False, help=argparse_help_messages["characters"]["help"])
    parser.add_argument("-charf","--characterfile", required=False, help=argparse_help_messages["characterfile"]["help"])
    parser.add_argument("-nfg","--noforeground",nargs="?", const=False, dest="foreground", required=False, help=argparse_help_messages["background"]["help"])
    parser.add_argument("-nbg","--nobackground",nargs="?", const=False, dest="background", required=False, help=argparse_help_messages["foreground"]["help"])

    return vars(parser.parse_args())

def processInputs(arguments,raw_arguments):
    #TODO many values need validation (add vlidation in the appropriate places) (value range validation)
    for key in raw_arguments.keys():
        if raw_arguments[key]!=None:
            match key:
                case "contrast" | "contrastbreak" | "blur":
                    arguments[key]=float(raw_arguments[key])
                case "sample_size":
                    arguments[key]=processSampleSize(raw_arguments[key]) #tuple [w,h]
                case "characters":
                    arguments[key]=processCharacters(raw_arguments[key]) #str
                case _:
                    arguments[key]=raw_arguments[key]
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