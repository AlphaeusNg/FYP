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

    def perform_translation(self):
        # Translate each OCR result to English
        translated_results = []

        for bbox, text, conf in self.localised_text:
            translated_text = translate.translate_language(text=text, language="en", still_in_development=True)
            self.localised_text

    def overlay_text(self):
        # Overlay translated text onto the image
        easy_ocr.overlay_text(self.image_path, self.translated_results)
    
    def process_image(self):
        self.perform_ocr()
        self.perform_translation()
        self.overlay_text()

if __name__ == "__main__":
    # Example usage
    image_path = Path("uploads\Tsuihou Sareta Tenshou Juu Kishi wa game Chishiki de Musou Suru Chapter 64 Raw - Rawkuma-03.png")
    image = image_object(image_path)
    image.process_image()
    print("Text overlayed on image.")  # Output: "Text overlayed on image."
    # show image
