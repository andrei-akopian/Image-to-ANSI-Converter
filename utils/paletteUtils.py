import json

def loadPalette(palettename,palette,ColorPoint):
    #open file
    if not("/" in palettename):
        palettename="palettes/"+palettename+".json"
    data={}
    with open(palettename,"r") as f:
        data=json.load(f)
    #create palette
    palette.muteable=False
    palette.monopattern=data["monopattern"]
    palette.duopattern=data["monopattern"]
    for cp in data["colors"]:
        palette.addpoint(ColorPoint(cp[2]))
        palette.colorPoints[-1].foreground=cp[0]
        palette.colorPoints[-1].background=cp[1]

    return palette

