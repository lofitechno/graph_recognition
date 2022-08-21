import cv2
import numpy as np

image= cv2.imread('C:/aurorealis/420lab/imgs/graph1.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
small = cv2.resize(image, (0,0), fx=0.2, fy=0.2)
th = cv2.adaptiveThreshold(small,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
th2 = cv2.adaptiveThreshold(small,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
ret,th0 = cv2.threshold(small,150,255,cv2.THRESH_BINARY)



cv2.imshow("sd", th0)
cv2.waitKey(0)
