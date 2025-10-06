import easyocr
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import cv2
app=FastAPI()

class Request(BaseModel):
    image_path:str

@app.post("/mrz")
async def mrz_extraction(request:Request):
    try:
        ans=extract_mrz_easy(request.image_path)
        return ans
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def extract_mrz_easy(image_path):
    img=cv2.imread(image_path)
    h,w=img.shape[:2]
    lower_part=img[int(h*0.80):h,0:w]
    gray=cv2.cvtColor(lower_part,cv2.COLOR_BGR2GRAY)
    
    # Initialize EasyOCR
    reader = easyocr.Reader(['en'], gpu=False, verbose=False)  # Set gpu=True if you have CUDA
    cv2.imwrite("gray.png",gray)
    # Run OCR
    result = reader.readtext(gray,detail=0)
    n=len(result)

    mrz_lines = []
    for detection in result:
        text = detection
        mrz_lines.append(text)
    print("📄 Detected MRZ lines:",mrz_lines)
    return {
        "first":result[n-2],
        "second":result[n-1]
    }

ans1=extract_mrz_easy("IND.png")
print("EasyOCR Result:\n", ans1)