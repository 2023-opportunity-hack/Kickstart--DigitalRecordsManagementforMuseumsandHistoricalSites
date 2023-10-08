from PIL import Image
import pytesseract

# Open the scanned newspaper image using PIL (Pillow)
image = Image.open('test_files/newspaper.jpeg')

# Perform OCR using pytesseract
text = pytesseract.image_to_string(image)

print(text)