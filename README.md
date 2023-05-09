# Image to ANSI converter
A tool for converting images into ANSI arts. Written in python using Pillow image processing library. The scripts support comand line arguments, so you won't have to modify the code directly. I made this tool due to a lack of "proper" similar tools with sufficient customization and options.

### Requirements
- Python (3)
- baisic knowledge of terminals, filepaths and commandline argument usage.
- Python pillow library
- Image in a format that Pillow can open (`.png .jpg .jpeg`)

## Usage
As I said, you can use the program enitrely formt the commandline.

### Setup
I haven't made any advanced setup, so you will have to download a zip of the repo, extract it whereever you want and `cd` into the extracted folder. Prepare the image you want to convert, I recomend placing it into the same folder, but using a filepath to some different location is also supported.

### Use
Type `python3 main.py -h` into the commandline to display the help message.

Here is a summery of the commandline arguments:

`-f --filename` is the filepath to your image, the default image name is image.png.

`-s --sampleSize` is the size of the samples, default is 16 (the output will be 16x smaller)

`-c --contrast` allows you to change the contrast of the image for better results. (recomended 1 - 1.2 range)

`-cb --contrastbreak` is the border of darkness levels between making a pixel darker or brighter (0-255 recomended range 50-200)

`-o --output` specify output file it can be then displayed with `cat output.txt` with all the colors

## TODO
- [ ] improve smapling algorithm
- [ ] add forground or background only
- [ ] make better output file handler (file formats)
- [ ] improve contrast algorithm
- [ ] make "setsize" instead of sampleSize- it is not user friendly
- [ ] contrast is probably messing with the sampling algorithm
- [ ] add examples to readme
- [ ] add option to display or not display as it is being created
- [ ] better character sets

