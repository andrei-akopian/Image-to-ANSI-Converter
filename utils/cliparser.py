import argparse

def parse(ArgsParserArguments):
    parser=argparse.ArgumentParser(
        prog="Image to ANSI converter"
    )

    parser.add_argument("-f","--filename",default=ArgsParserArguments["filename"],help="Filepath to your image, the default image name is image.png")
    parser.add_argument("-c","--contrast",default=ArgsParserArguments["contrast"],help="allows you to change the contrast of the image for better results. (recomended 1 - 1.2 range)")
    parser.add_argument("-s","--sampleSize",default=ArgsParserArguments["sampleSize"],help="Size of the samples, default is 16x16 (the output will be 16x smaller) enter as XxY or just X")
    parser.add_argument("-cb","--contrastbreak",default=ArgsParserArguments["contrastbreak"],help="Border of darkness levels between making a pixel darker or brighter (0-255 recomended range 50-200)")
    parser.add_argument("-o","--output",default=ArgsParserArguments["output"],help="Specify output file it can be then displayed with `cat output.txt` with all the colors")
    parser.add_argument("-b","--blur",default=ArgsParserArguments["blur"],help="Blurs a furhter range of colors")
    parser.add_argument("-p","--palettename",default=ArgsParserArguments["palettename"],help="Enter name of the pallete from palettes or file path")
    parser.add_argument("--hide", action='store_const',const=False, default=ArgsParserArguments["display"], help="if false (default) will display the image as it is being generated")
    parser.add_argument("-char","--characters", default=ArgsParserArguments["characters"], help="enter characters")
    parser.add_argument("-charf","--characterfile", default=ArgsParserArguments["characterfile"], help="enter characters")

    return parser.parse_args()