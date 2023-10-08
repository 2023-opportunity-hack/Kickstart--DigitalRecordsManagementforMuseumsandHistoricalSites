from PIL import Image
import pytesseract
def image_process(image_path):
    image = Image.open(image_path)
    
    # Understand the image

    # Get text from image
    text = pytesseract.image_to_string(image)
