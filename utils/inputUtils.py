
"""
Read, load, cli, configs and other inputs
"""

import yaml
import os
import sys
from PIL import Image
import math

def getYamlFile(filepath):
    with open(filepath,"r") as f:
        return yaml.safe_load(f)

def getInput():
    raw_arguments=parsecli()

    if "argumentfile" in raw_arguments.keys():
        arguments=getYamlFile(raw_arguments["argumentfile"])
    else:
        arguments=getYamlFile("utils/defaultargumentfile.yaml")
    arguments=processInputs(arguments,raw_arguments)

    return arguments

def parsecli():
    """parses cli and makes a dictionary
    """
    arguments=sys.argv[1:]
    if len(arguments)==0:
        return {}
    # * help message
    elif arguments[0] in "--help":
        print("Fake print message")
        pass #FIXME create a help message generator

    parsecli_arguments=getYamlFile("utils/parsecliArguments.yaml")
    aliases=parsecli_arguments["aliases"]
    def convertAlias(alias):
        #check if is alias and return good value
        if alias in aliases.keys(): #alias
            return aliases[alias]
        else: #not an alias
            return alias
    raw_arguments={}
    current_key=None
    for argument in arguments:
        if argument[0]=="-":
            if "=" in argument:
                sign_position=argument.find("=")
                current_key=convertAlias(argument[:sign_position].strip("-"))
                argument=argument[sign_position+1:]
                raw_arguments[current_key]=argument
            else:
                current_key=convertAlias(argument.strip("-"))
                raw_arguments[current_key]=None
        else:
            raw_arguments[current_key]=argument
    return raw_arguments

def processInputs(arguments,raw_arguments):
    #TODO many values need validation (add vlidation in the appropriate places) (value range validation)
    for key in raw_arguments.keys():
        match key:
            case "contrast" | "contrastbreak" | "blur":
                arguments[key]=float(raw_arguments[key])
            case "output_filename":
                if raw_arguments[key]==None: #TODO make this cleaner when rewriting
                    arguments[key]="output.txt"
                else:
                    arguments[key]=raw_arguments[key]
            case "hide":
                arguments[key]=not(processBool(raw_arguments[key]))
            case "sample_size":
                arguments[key]=processSampleSize(raw_arguments[key]) #tuple [w,h]
            case "characters":
                arguments[key]=processCharacters(raw_arguments[key]) #str
            case "noforeground" | "nobackground":
                arguments[key[2:]]=processGrounds(raw_arguments[key]) #bool or str
            case _:
                arguments[key]=raw_arguments[key]
    return arguments

def processBool(value):
    if value in [None, "0","off","f","false","False"]:
        return False
    elif value in ["1","on","t","true","True"]:
        return True
    else:
        return None

def processGrounds(ground):
    ground_bool=processBool(ground)
    if ground==None:
        return ground
    else:
        return ground_bool

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
        if type(output_size)==str: #* if it's a list, the job is done already
            if output_size=="fill":
                output_size=os.get_terminal_size()
            else:
                try:
                    output_size=list(map(int,output_size.split("x")))
                    if len(output_size)!=2:
                        raise Exception(f"\033[1m Incorrect --output_size input. Specify as WxH eg. 20x20")
                except:
                    raise Exception(f"\033[1m Bad --output_size input. Specify as WxH eg. 20x20")
        sample_size[0],sample_size[1]=math.floor(image_size[0]/output_size[0]),math.floor(image_size[1]/output_size[1])

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