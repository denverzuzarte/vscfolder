from pathlib import Path
from PIL import Image
import random
import math
def trainer(location):
    image = Image.open(location)
    arr=[];
    x=0;
    while x < 28:
        arr.append([]);
        y=0;
        while y <28:
            arr[x].append(image.getpixel((x,y))[3]/255);
            y=y+1;
        x=x+1;
    return arr;