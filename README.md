# py-Emojisaic

## python implementation of [Emojisaic](https://github.com/lilkraftwerk/Emojisaic)

### Install
```
git clone https://github.com/hrnggg/py-Emojisaic
cd py-Emojisaic
pip install -r requirements.txt
```

### How to use
```
python3 emojisaic.py -i [filename.jpg] (for still image) or 
python3 emojisaic.py -g [fielname.gif] (for a gif)
```

### Options
- -s, --size [int] - emoji height in pixels (default: 8)
- -z, --zoom [int] - multiply size of original image by this (default: 1)
- -o, --offset [int] - random offset for emoji placement, in pixels (default: 0)                          
- -c, --coverage [int] - generally the emoji finder will use the emoji that is closest to the color for a given pixel area. setting this will prefer emojis with fewer transparent pixels which sometimes looks better
- -q, --quiet - be quiet! no output in this mode
- -t, --tmp - remove all temp files (use by itself)
- --help - show options
