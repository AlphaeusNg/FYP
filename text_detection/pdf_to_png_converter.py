import fitz  # PyMuPDF
from PIL import Image
import os


def convert_pdf_to_png(image_path, output_folder):
    # Check if the image path ends with .pdf
    if image_path.lower().endswith('.pdf'):
        # Run the pdf_to_png function
        png_image_paths = pdf_to_png(image_path, output_folder)
        print(f"PDF converted to PNG images. Output folder: {output_folder}")
        return png_image_paths
    else:
        print("The provided file is not a PDF.")


def pdf_to_png(pdf_path, output_folder):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # List to store paths of saved PNG images
    png_image_paths = []

    # Iterate through each page
    for page_number in range(pdf_document.page_count):
        # Get the page
        page = pdf_document[page_number]

        # Convert the page to an image
        image = page.get_pixmap()

        # Create PIL Image from raw data
        pil_image = Image.frombytes("RGB", [image.width, image.height], image.samples)

        # Save the image as PNG
        output_path = f"{output_folder}/page_{page_number + 1}.png"
        pil_image.save(output_path, format="PNG")

        # Append the path to the list
        png_image_paths.append(output_path)

    # Close the PDF file
    pdf_document.close()

    return png_image_paths


if __name__ == "__main__":
    current_directory = os.getcwd()
    pdf_path = current_directory + "/images/Tsuihou Sareta Tenshou Juu Kishi wa game Chishiki de Musou Suru Chapter 64 Raw - Rawkuma.pdf"
    output_folder = current_directory + "/images/output/pdf_to_png"
    os.makedirs(output_folder, exist_ok=True)
    convert_pdf_to_png(pdf_path, output_folder)