Notate as json:
```json
{
    "monopattern" : "{ESC}[{color}m",
    "duopattern" : "{ESC}[{foreground}m{ESC}[{background}m",
    "foreground_prefix": "38:5:", //depends of what bit number of ANSI you are using in your palette
    "background_prefix": "48:5:", //lower bit size versions generate smaller --output .txt files

    // Configuration used if no palette is specified:
    // self.monopattern="{ESC}[{color}m"
    // self.duopattern="{ESC}[{foreground}m{ESC}[{background}m"
    // self.foreground_prefix="38;2;"
    // self.background_prefix="48;2;"

    "colors" : [
        [[0,0,0],"foreground","background"] //filterpalettes don't need the last 2
    ]
}
```
#TODO improve palettes, add muteable to palette, and weight for points
For filter palettes the first 4 keys are not really required, but the rgb tuple has to be on the 3rd spot, you can just out empty strings into the first 2
