from pathlib import Path
from language_translation import translate
from text_detection.pdf_to_png_converter import convert_pdf_to_png
from text_detection import easy_ocr
from PIL import Image

class image_object:
    
    def __init__(self, image_path: Path=None, image: Image=None, localised_text: list[str]=[], original_lang_code: str=None, translated_lang_code: str=None):
        self.image_path = image_path if image_path is not None else None
        self.image = Image.open(image_path) if image is None else image
        self.localised_text = [] if localised_text is None else localised_text
        self.original_lang_code = "en" if original_lang_code is None else original_lang_code
        self.translated_lang_code = "zh" if translated_lang_code is None else translated_lang_code

    def perform_ocr(self, output_folder, language_code:list[str]=["en"]):
        # Perform OCR on the provided image file
        if self.image_path:
            self.localised_text = easy_ocr.text_inference(self.image_path, output_folder=output_folder, language_code=language_code, annotate=True)
        elif self.image:
            self.localised_text = easy_ocr.text_inference(self.image, output_folder=output_folder, language_code=language_code, annotate=True)
        else:
            raise ValueError("No image or image path provided for OCR.")

    def perform_translation(self, original_language: str="English", translated_language: str="Chinese"):

        for i, (bbox, text) in enumerate(self.localised_text):
            translated_text = translate.translate_language(text=text, original_language=original_language, translated_language=translated_language, development_mode=False) #TODO
            self.localised_text[i] = (bbox, text, translated_text)
            

    def overlay_text(self):
        # Overlay translated text onto the image
        self.image = easy_ocr.overlay_text(self.image_path, self.localised_text, lang_code=self.translated_lang_code)
    
    def process_image(self, output_folder, original_language: str="English", translated_language: str="Chinese", language_code:list[str]=["en"]):
        self.perform_ocr(output_folder, language_code=language_code)
        self.perform_translation(original_language=original_language, translated_language=translated_language)
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
    # file_dir = "AisazuNihaIrarenai"
    folder_dir = Path(r"C:\Users\alpha\OneDrive\Desktop\Life\NTU\FYP\FYP\images\The Exiled Reincarnated Heavy Knight Is Unrivaled In Game Knowledge - Chapter 64 - Aqua manga\The Exiled Reincarnated Heavy Knight Is Unrivaled In Game Knowledge - Chapter 64 - Aqua manga-04.png")
    # folder_name = Path(r"The Exiled Reincarnated Heavy Knight Is Unrivaled In Game Knowledge - Chapter 64 - Aqua manga-04.png")
    folder_dir = current_directory / folder_dir
    # image_path = current_directory / "images" / file_dir / file_name
    output_folder = current_directory / "images" / "output" / "easyocr" / folder_dir.name
    os.makedirs(output_folder, exist_ok=True)

    if folder_dir.is_dir():
        for count, file in enumerate(os.listdir(folder_dir)):
            file_path = folder_dir / file
            image = image_object(file_path, original_lang_code="English", translated_lang_code="Chinese")
            image.process_image(output_folder=output_folder, 
                                original_language="English", 
                                translated_language="Chinese", 
                                language_code=["en"])
            image.save_image(output_folder / f"translated_image_{count}.png")
            print("Text overlayed on image.")
    else:
        image = image_object(folder_dir, original_lang_code="English", translated_lang_code="Chinese")
        image.process_image(output_folder=output_folder, 
                            original_language="English", 
                            translated_language="Chinese", 
                            language_code=["en"])
        image.save_image(output_folder / f"translated_image_{99}.png")
        print("Text overlayed on image.")