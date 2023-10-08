import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
import PyPDF2

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = T5ForConditionalGeneration.from_pretrained("Michau/t5-base-en-generate-headline")
tokenizer = T5Tokenizer.from_pretrained("Michau/t5-base-en-generate-headline")
model = model.to(device)


def extract_text_from_pdf(pdf_file_path):
    text = ""
    try:
        with open(pdf_file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                # page = pdf_reader.getPage(page_num)
                text += page.extract_text()
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
    return text


# article = extract_text_from_pdf("image_test.pdf")
# article = extract_text_from_pdf("image_windmill.historypage.wpd.docx.pdf")
article = extract_text_from_pdf("SIGNIFICANT BUILDINGS.doc.pdf")
print(article)


text = "headline: " + article

max_len = 256

encoding = tokenizer.encode_plus(text, return_tensors="pt")
input_ids = encoding["input_ids"].to(device)
attention_masks = encoding["attention_mask"].to(device)

beam_outputs = model.generate(
    input_ids=input_ids,
    attention_mask=attention_masks,
    max_length=64,
    num_beams=3,
    early_stopping=True,
)

result = tokenizer.decode(beam_outputs[0])
print(result)
