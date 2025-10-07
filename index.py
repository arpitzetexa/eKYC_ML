import easyocr
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import cv2
import numpy as np
import urllib.request
app=FastAPI()

class Request(BaseModel):
    url_path:str

@app.get("/")
def get_root_url():
    return {"message":"Welcome to the eKYC API"}

@app.post("/mrz")
async def mrz_extraction(request:Request):
    try:
        ans=extract_mrz_easy(request.url_path)
        return {
            "status_code":200,
            "passport_details":ans
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def extract_mrz_easy(image_path):
    resp = urllib.request.urlopen(image_path)
    image_data = np.asarray(bytearray(resp.read()), dtype=np.uint8)
    img = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    h,w=img.shape[:2]
    lower_part=img[int(h*0.70):h,0:w]
    gray=cv2.cvtColor(lower_part,cv2.COLOR_BGR2GRAY)
    
    # # Threshold to binary
    # thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # # Find all coordinates of rotated text
    # coords = np.column_stack(np.where(thresh > 0))

    # # Get minimum area rectangle
    # angle = cv2.minAreaRect(coords)[-1]

    # # Adjust angle
    # if angle < -45:
    #     angle = -(90 + angle)
    # else:
    #     angle = -angle

    # # Rotate image
    # (h, w) = img.shape[:2]
    # center = (w // 2, h // 2)
    # M = cv2.getRotationMatrix2D(center, angle, 1.0)
    # rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    
    # Initialize EasyOCR
    reader = easyocr.Reader(['en'], gpu=False, verbose=False)
    cv2.imwrite("rotated.png",gray)
    
    # Run OCR
    result = reader.readtext(gray)

    n=len(result)
    confidence_line1=result[n-2][2]
    confidence_line2=result[n-1][2]

    line1=result[n-2][1]
    line2=result[n-1][1]
    
    if(len(line1)!=44 or len(line2)!=44 or confidence_line1<0.7 or confidence_line2<0.7):
        raise HTTPException(
                            status_code=400,
                            detail="MRZ lines not detected properly. Please provide a clear image of the passport.")
    first_name=""
    surname=""
    flag=False
    index=5

    while(index<44):
        if(flag==False):
            if(line1[index]=='<' and line1[index+1]=='<'):
                flag=True
                index+=2
                continue
            else:
                surname+=line1[index]
        else:
            if(line1[index]=='<' and line1[index+1]=='<'):
                break
            elif(line1[index]=='<'):
                first_name+=' '
            else:
                first_name+=line1[index]
        index+=1

    nationality=line1[2:5]
    passport_number=line2[0:9].replace("<","")
    passport_check=line2[9]
    birth_date=line2[13:19]
    birth_check=line2[19]
    gender=line2[20]
    expiry_date=line2[21:27]
    expiry_check=line2[27]

    return {
        "first_name":first_name,
        "last_name":surname,
        "nationality":nationality,
        "passport_number":passport_number,
        "passport_check":passport_check,
        "birth_date":birth_date,
        "birth_check":birth_check,
        "gender":gender,
        "expiry_date":expiry_date,
        "expiry_check":expiry_check
    }


ans1=extract_mrz_easy("https://www.immihelp.com/assets/article-images/sample-indian-passport-1.jpg")
print("EasyOCR Result:\n", ans1)