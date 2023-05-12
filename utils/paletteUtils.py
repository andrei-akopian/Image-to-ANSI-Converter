import json

#TODO the pal functions are currently unused
def load_pal(filename):
    """reads a .pal file and exports all colors as rgb tuples

    #< filename: path to the .pal file you want to load

    #> list of tuples of the colors in the palette
    """
    with open(filename, 'rb') as f:
        f.read(4)
        colors = []
        while True:
            color_bytes = f.read(3)
            if not color_bytes: #EOF
                break
            color = tuple(color_bytes)
            colors.append(color)
    return colors

def save_pal(filename, colors):
    """saves a list of rgb tuples as a .pal file

    #< filename: name of the file you want to save to
    #< colors: list of rgb tuples you want to save 
    """
    with open(filename, 'wb') as f:
        f.write(b'RIFF') #filetype indetifier
        for color in colors:
            r, g, b = color
            f.write(bytes([r, g, b]))

def loadPalette(palettename):
    if not("/" in palettename):
        palettename="palettes/"+palettename+".json"
    palette={}
    with open(palettename,"r") as f:
        palette=json.load(f)
    
    #TODO rename everything to anchorColors
    anchorColors = [[color[2], 1] for color in palette["colors"]]
    return palette, anchorColors

