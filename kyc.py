import cv2 as cv

def resizedImage(height,img_Path):
    target_height=height
    img=cv.imread(img_Path)
    height=img.shape[0]
    width=img.shape[1]
    aspect_ratio=height/width
    target_width=int(aspect_ratio*target_height)
    img=cv.imread("Island.jpg")
    resized_image=cv.resize(img,(target_height,target_width),interpolation=cv.INTER_LINEAR)
    return resized_image

img=cv.imread("Jennifer.jpg")
cv.imshow("Jennifer",img)
b,g,r=cv.split(img)
mrg=cv.merge([r,g,b])

cv.imshow("Merged_Jennifer",mrg)
cv.waitKey(10000)
