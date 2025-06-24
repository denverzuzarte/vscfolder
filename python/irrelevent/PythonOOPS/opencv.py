import cv2 as cv;
import numpy as np;
import pandas as pd;
import math;
import random;
import rgbtohsv as hsv;
import time;
img = cv.imread(r'C:\Users\Denver Zuzarte\vsc folder\python\PythonOOPS\images\img.jpg');
(B,G,R)=img[2001,2000];
print(B,G,R);
h,s,v=hsv.rgb_to_hsv(R,G,B);
print (h,s,v);
'''
img2=[];
j=0;
# converting the image into hsv type shi
for a in img :
    img2.append([]);
    for b in a:
        img2[j].append(hsv.rgb_to_hsv(b[0],b[1],b[2]));
    j=j+1;
print(img2);
'''
'''
# Extracting the height and width of an image
h, w = img.shape[:2];
# Displaying the height and width
print("Height = {}, Width = {}".format(h, w));
'''
'''
# We will show the region of interest
# by slicing the pixels of the image
roi = img[500 : 2500, 200 : 2700];
cv.imshow("ROI", roi);
cv.waitKey(0);
'''
# resize the image and the dimensions
resize = cv.resize(img, (500, 500))
#cv.imshow("Resized Image", resize)
#cv.waitKey(0)
'''
#cv.imshow("help",resize);
#cv.waitKey(0);
#drawing a rectangle
output=resize.copy();
rect=cv.rectangle(output,(100,100),(200,300),(0,255,255),5);
cv.imshow("k",rect);
# Copying the original image
output = resize.copy()

# Adding the text using putText() function
text = cv.putText(output, 'OpenCV Demo', (200, 250),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2);
cv.imshow("hwloo",text);
'''
# Import opencv
import cv2

# Use the second argument or (flag value) zero
# that specifies the image is to be read in grayscale mode
img = cv2.imread('', 0)

cv2.imshow('Grayscale Image', img)
cv2.waitKey(0)

# Window shown waits for any key pressing event
cv2.destroyAllWindows()