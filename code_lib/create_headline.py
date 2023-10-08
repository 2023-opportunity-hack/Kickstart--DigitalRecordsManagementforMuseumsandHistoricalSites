import torch
# import SentencePiece
# extract text from PDF
import PyPDF2

from transformers import (
    # headline generation libraries
    T5ForConditionalGeneration,
    T5Tokenizer,

    # extract significant text libraries
    TokenClassificationPipeline,
    AutoModelForTokenClassification,
    AutoTokenizer,
)

# for significant text tag generation
from transformers.pipelines import AggregationStrategy
import numpy as np

# PDF TEXT EXTRACTION
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

# HEADLINE GENERATION
def headline_generation(article):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = T5ForConditionalGeneration.from_pretrained("Michau/t5-base-en-generate-headline")
    tokenizer = T5Tokenizer.from_pretrained("Michau/t5-base-en-generate-headline")
    model = model.to(device)
    max_len = 256
    encoding = tokenizer.encode_plus(article, return_tensors="pt")
    input_ids = encoding["input_ids"].to(device)
    attention_masks = encoding["attention_mask"].to(device)
    beam_outputs = model.generate(
        input_ids=input_ids,
        attention_mask=attention_masks,
        max_length=64,
        num_beams=3,
        early_stopping=True,
    )

    headline = tokenizer.decode(beam_outputs[0])
    return headline
# KEYPHRASE EXTRACTION
# Define keyphrase extraction pipeline
def KeyphraseExtration(article):
    class KeyphraseExtractionPipeline(TokenClassificationPipeline):
        def __init__(self, model, *args, **kwargs):
            super().__init__(
                model=AutoModelForTokenClassification.from_pretrained(model),
                tokenizer=AutoTokenizer.from_pretrained(model),
                *args,
                **kwargs
            )

        def postprocess(self, all_outputs):
            results = super().postprocess(
                all_outputs=all_outputs,
                aggregation_strategy=AggregationStrategy.FIRST,
            )
            return np.unique([result.get("word").strip() for result in results])

    # Load pipeline
    model_name = "ml6team/keyphrase-extraction-distilbert-inspec"
    extractor = KeyphraseExtractionPipeline(model=model_name)
    keyphrases = extractor(article)
    return keyphrases



file_path = "test_files/SIGNIFICANT BUILDINGS.doc.pdf"

if file_path.endswith(".pdf"):
    article = "headline: " + extract_text_from_pdf(file_path)
else:
    print("File type not recognized")

headline = headline_generation(article)
keyphrases = KeyphraseExtration(article)
# PRINT HEADLINE AND KEYPHRASES
print(headline)
print(keyphrases)
