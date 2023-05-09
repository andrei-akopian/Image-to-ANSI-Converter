import argparse

#parse cli arguments
defaultFile="test.png"

parser=argparse.ArgumentParser(
    prog="Image to ANSI converter"
)
parser.add_argument("-f","--filename",default=defaultFile)
parser.add_argument("-c","--contrast",default=1)
parser.add_argument("-s","--sampleSize",default=16)
parser.add_argument("-cb","--contrastbreak",default=128)
args=parser.parse_args()

with open("converter.py","r") as f:
    code=f.read()
exec(compile(code,"converter","exec"))