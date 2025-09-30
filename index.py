import cv2 
import pytesseract
from passporteye import read_mrz
from PIL import Image

# (Optional) Only needed on Windows, set Tesseract path:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image_path):
    # Load image
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Denoise
    denoised = cv2.medianBlur(gray, 3)

    # Adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        denoised, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 31, 2
    )

    # Morphological cleanup
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    # Resize to improve OCR
    resized = cv2.resize(morph, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    return resized

def extract_text(image_path):
    processed = preprocess_image(image_path)
    # OCR with Tesseract
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(processed, config=custom_config)
    return text

def extract_mrz(image_path):
    mrz = read_mrz(image_path)
    if mrz is None:
        return None
    return mrz.to_dict()

img_path = "./Island.jpg"
mrz_data = extract_mrz(img_path)
text=mrz_data['raw_text']

nationality=''
nationality+=text[2]+text[3]+text[4]
first_name=''
last_name=''

index=-1

for i in range(5,len(text)+1):
    if(text[i]=='<' and text[i+1]=='<'):
        index=i+2
        break
    else:
        last_name+=text[i]

passport_number=''
index2=45
while(index2<=53):
    if(text[index2]!='<'):
        passport_number+=text[index2]
        index2=index2+1
    else:
        break

ind=58
dob=''
expiry_date=''
gender=''

for i in range(index,len(text)+1):
    if(text[i]=='<' and text[i+1]=='<'):
        break

    elif(text[i]=='<' and text[i+1]!='<'):
        first_name+=' '

    else:
        first_name+=text[i]


print(nationality,first_name,last_name,passport_number)



