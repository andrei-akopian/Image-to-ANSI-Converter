import argparse

#parse cli arguments
parser=argparse.ArgumentParser(
    prog="Image to ANSI converter"
)
parser.add_argument("-f","--filename",default="image.png",help="Filepath to your image, the default image name is image.png")
parser.add_argument("-c","--contrast",default=1,help="Size of the samples, default is 16 (the output will be 16x smaller)")
parser.add_argument("-s","--sampleSize",default=16,help="allows you to change the contrast of the image for better results. (recomended 1 - 1.2 range)")
parser.add_argument("-cb","--contrastbreak",default=128,help="Border of darkness levels between making a pixel darker or brighter (0-255 recomended range 50-200)")
parser.add_argument("-o","--output",default=None,help="Specify output file it can be then displayed with `cat output.txt` with all the colors")
args=parser.parse_args()

with open("converter.py","r") as f:
    code=f.read()
exec(compile(code,"converter","exec"))