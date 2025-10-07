import cv2 
import numpy as np
import easyocr
img = cv2.imread("Zet1.jpeg")
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
reader=easyocr.Reader(['en'],gpu=False,verbose=False)
result=reader.readtext(gray)
n=len(result)
confidence_line1=result[n-2][2]
confidence_line2=result[n-1][2]
print(confidence_line1,confidence_line2)

    
    # Threshold to binary
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)[1]
thresh = cv2.bitwise_not(thresh)
    # Find all coordinates of rotated text
coords = np.column_stack(np.where(thresh > 0))
    # Get minimum area rectangle
angle = cv2.minAreaRect(coords)[-1]

    # Adjust angle
if angle < -45:
    angle = (90 + angle)
else:
    angle = angle

    # Rotate image
(h, w) = img.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

cv2.imshow("rotated",rotated)
cv2.waitKey(0)
cv2.destroyAllWindows()
    