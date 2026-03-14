from pypdf import PdfReader, PdfWriter
import math
import os

pdf_path = "Dahua_Network_Speed_Dome_PTZ_Camera_Web_5.0_User_s_Manual_V1.2.1.pdf"

print(f"Leyendo el archivo: {pdf_path}")
reader = PdfReader(pdf_path)
total_pages = len(reader.pages)
print(f"Total de páginas: {total_pages}")

# Calculate pages per split file (6 parts to ensure under 10MB)
parts = 6
pages_per_split = math.ceil(total_pages / parts)

for i in range(parts):
    writer = PdfWriter()
    start_page = i * pages_per_split
    end_page = min((i + 1) * pages_per_split, total_pages)
    
    for page_num in range(start_page, end_page):
        writer.add_page(reader.pages[page_num])
    
    output_filename = f"Parte_{i+1}_Manual_Dahua.pdf"
    with open(output_filename, "wb") as output_pdf:
        writer.write(output_pdf)
    
    size_mb = os.path.getsize(output_filename) / (1024 * 1024)
    print(f"Creado: {output_filename} (Páginas {start_page+1} a {end_page}) - Tamaño: {size_mb:.2f} MB")
