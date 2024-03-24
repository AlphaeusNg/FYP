from pathlib import Path
from language_translation import translate
from text_detection.pdf_to_png_converter import convert_pdf_to_png
from text_detection import easy_ocr
from PIL import Image

class image_object:
    
    def __init__(self, image_path: Path=None, image: Image=None, localised_text: list[str]=[]):
        self.image_path = image_path if image_path is not None else None
        self.image = Image.open(image_path) if image is None else image
        self.localised_text = [] if localised_text is None else localised_text

    def perform_ocr(self):
        # Perform OCR on the provided image file
        if self.image_path:
            self.localised_text = easy_ocr.text_inference(self.image_path, annotate=True)
        elif self.image:
            self.localised_text = easy_ocr.text_inference(self.image, annotate=True)
        else:
            raise ValueError("No image or image path provided for OCR.")

    def perform_translation(self, translation_language: str="en"):

        for i, (bbox, text) in enumerate(self.localised_text):
            translated_text = translate.translate_language(text=text, language=translation_language, still_in_development=True)
            self.localised_text[i] = (bbox, text, translated_text)
            

    def overlay_text(self):
        # Overlay translated text onto the image
        self.image = easy_ocr.overlay_text(self.image_path, self.localised_text)
    
    def process_image(self, language: str="en"):
        self.perform_ocr()
        self.perform_translation(translation_language=language)
        self.overlay_text()
    
    def save_image(self, output_path: Path):
        self.image.save(output_path)
        return output_path

if __name__ == "__main__":
    # Example usage
    import os
    current_directory = Path.cwd()
    # file_dir = "Tsuihou Sareta Tenshou Juu Kishi wa game Chishiki de Musou Suru Chapter 64 Raw - Rawkuma"
    # file_name = "Tsuihou Sareta Tenshou Juu Kishi wa game Chishiki de Musou Suru Chapter 64 Raw - Rawkuma-04.png"
    file_dir = "AisazuNihaIrarenai"
    folder_dir = current_directory / "images" / file_dir
    # image_path = current_directory / "images" / file_dir / file_name
    output_folder = current_directory / "images" / "output" / "easyocr" / file_dir
    os.makedirs(output_folder, exist_ok=True)

    for count, file in enumerate(os.listdir(folder_dir)):
        file_path = folder_dir / file
        image = image_object(file_path)
        image.process_image()
        image.save_image(output_folder / f"translated_image_{count}.png")
        print("Text overlayed on image.")
