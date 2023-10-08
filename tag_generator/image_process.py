from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import pytesseract

def image_process(image_path):
    image = Image.open(image_path)
    raw_image = Image.open(image_path).convert('RGB')
    
    # Understand the image
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
    inputs = processor(raw_image, return_tensors="pt")

    out = model.generate(**inputs)
    image_context = processor.decode(out[0], skip_special_tokens=True)

    # Get text from image
    text = pytesseract.image_to_string(image)
    tags = text.split('\n')

    tags.append(image_context)
    return {"file":image_path,"tags":tags}
