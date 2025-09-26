import cv2
import easyocr

# Step 1: Load image
img = cv2.imread("Island.jpg")

# Step 2: Preprocess
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)          # Grayscale
denoised = cv2.medianBlur(gray, 3)                    # Remove noise

# Step 3: Threshold (binarization)
_, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Step 4: (Optional) Resize to improve OCR on small text
scale_percent = 200  # enlarge by 200%
w = int(thresh.shape[1] * scale_percent / 100)
h = int(thresh.shape[0] * scale_percent / 100)
resized = cv2.resize(thresh, (w, h), interpolation=cv2.INTER_LINEAR)

# Step 5: OCR with EasyOCR
reader = easyocr.Reader(['en', 'fr', 'hi', 'de', 'ja'])  # Add languages you expect
results = reader.readtext(resized)

# Step 6: Print extracted text
for (bbox, text, prob) in results:
    print(f"Detected: {text} (Confidence: {prob:.2f})")

# (Optional) Show processed image
cv2.imshow("Processed", resized)
cv2.waitKey(0)
cv2.destroyAllWindows()
