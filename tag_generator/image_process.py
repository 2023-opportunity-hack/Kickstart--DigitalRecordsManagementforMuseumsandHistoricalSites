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
    
    newspaper_flag = False
    if "newspaper" in (image_context.lower()):
        print("Given photo is likely scan of newspaper")
        newspaper_flag = True



    # Get text from image
    text = pytesseract.image_to_string(image)
    print(text)
    # tags = text.split('\n')

    image_text = text + image_context
    
    text_file = open("Output.txt", "w")
    text_file.write(image_text)
    text_file.close()

    import text_process
    import os
    output = text_process.text_process("Output.txt")

    if newspaper_flag:
        output["tags"] = output["tags"].append("Newspaper Scan")
    else:
        output["tags"] = output["tags"].append("Image")
    os.remove("Output.txt")
    return output

    # tags.append(image_context)
    # return {"file":image_path,"tags":tags}
