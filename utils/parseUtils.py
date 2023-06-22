import argparse

def parse(ArgsParserArguments): #TODO rewrite it so that all the parameters can be specified in yaml
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
    parser.add_argument("-nbg","--nobackground",nargs='?',default=ArgsParserArguments["foreground"]["default"],const=False, dest="background", help=ArgsParserArguments["foreground"]["help"])

    return parser.parse_args()

def loadSampleSize(raw_sampleSize):
    if "x" in sampleSize:
        sampleSize=list(map(int,sampleSize.split("x")))
    else:
        sampleSize=int(sampleSize)
        sampleSize=[sampleSize,sampleSize]