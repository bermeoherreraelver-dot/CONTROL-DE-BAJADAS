import os
from pypdf import PdfReader

def extract_to_file(pdf_name, output_file):
    try:
        reader = PdfReader(pdf_name)
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                output_file.write(f"\n--- {pdf_name} - Page {i+1} ---\n")
                output_file.write(text)
    except Exception as e:
        output_file.write(f"\nError reading {pdf_name}: {e}\n")

with open("extract_pdfs.txt", "w", encoding="utf-8") as f:
    extract_to_file("EETT DE CCVT.pdf", f)
    extract_to_file("MD DE CCTV.pdf", f)
