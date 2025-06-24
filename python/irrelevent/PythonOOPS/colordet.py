import cv2 
import numpy as np 
import rgbtohsv as hsv;
import os

#defining how to read colour

def colour(img):
    pix=hsv.rgb_to_hsv(img[0],img[1],img[2]);
    if img[2]<30:
        return"black";
    elif img[2]>200 and img[1]<30:
        return "white";
    else:
        if -30<pix[0]<30:
            return "red";
        elif -30<pix[0]-60<30:
            return "yellow";
        elif -30<pix[0]-120<30:
            return "green";
        elif -30<pix[0]-180<30:
            return "cyan";
        elif -30<pix[0]-240<30:
            return "blue";
        elif -30<pix[0]-300<30:
            return "magenta";
        

# Read image. 
img = cv2.imread('python/PythonOOPS/images/circle3.png', cv2.IMREAD_COLOR) 
  
# Convert to grayscale. 
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
  
# Blur using 3 * 3 kernel. 
gray_blurred = cv2.blur(gray, (3, 3))

# Apply Hough transform on the blurred image. 
detected_circles = cv2.HoughCircles(gray_blurred,  
                   cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, 
               param2 = 30, minRadius = 1, maxRadius = 400) 

# Draw circles that are detected. 
if detected_circles is not None: 

    # Convert the circle parameters a, b and r to integers. 
    detected_circles = np.uint16(np.around(detected_circles)) 

    for pt in detected_circles[0, :]: 
        a, b, r = pt[0], pt[1], pt[2] 
  
        # Draw the circumference of the circle. 
        cv2.circle(img, (a, b), r, (0, 255, 0), 2) 
  
        # Draw a small circle (of radius 1) to show the center. 
        cv2.circle(img, (a, b), 1, (0, 0, 255), 3) 
        cv2.imshow("Detected Circle", img) 
        cv2.waitKey(0)
    print (colour(img[a][b])," circle found");