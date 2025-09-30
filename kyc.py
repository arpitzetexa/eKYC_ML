import cv2 as cv
import numpy as np

def resizedImage(height,img_Path):
    target_height=height
    img=cv.imread(img_Path)
    height=img.shape[0]
    width=img.shape[1]
    aspect_ratio=height/width
    target_width=int(aspect_ratio*target_height)
    img=cv.imread("amazon.jpg")
    resized_image=cv.resize(img,(target_height,target_width),interpolation=cv.INTER_LINEAR)
    return resized_image

img2=resizedImage(1600,"amazon.jpg")
cv.imshow("Hello",img2)
cv.waitKey(10000)