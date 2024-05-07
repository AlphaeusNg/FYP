from pathlib import Path
from PIL import Image
from typing import List, Tuple
from language_translation import translate
from text_detection import easy_ocr

class ImageObject:
    """
    Represents an image object with functionalities for OCR, translation, and overlaying text.
    """
    
    def __init__(self, image_path: Path = None, image: Image = None, localised_text: Tuple[List[float], str, str] = None,
                 original_lang_code: List[str] = None, translated_lang_code: List[str] = None):
        """
        Initializes an ImageObject instance.
        
        Args:
            image_path (Path, optional): Path to the input image. Defaults to None.
            image (Image, optional): PIL Image object. Defaults to None.
            localised_text (Tuple[List[float, float, float, float], str, str], optional): Localized text extracted from the image. Defaults to None.
            original_lang_code (List[str], optional): Language code of the original text. Defaults to None.
            translated_lang_code (List[str], optional): Language code of the translated text. Defaults to None.
        """
        self.image_path = image_path
        self.image = Image.open(image_path) if image_path else image
        self.localised_text = localised_text if localised_text is not None else []
        self.original_lang_code = original_lang_code
        self.translated_lang_code = translated_lang_code
        self.LANG_CODES_TO_NAMES = {
            "en": "English",
            "zh": "Chinese",
            "ja": "Japanese",
            "fr": "French",
            "it": "Italian",
            "pt": "Portuguese",
            "de": "German",
            "ru": "Russian",
        }

    # Setter for image_path attribute
    def set_image_path(self, image_path: Path) -> None:
        if not isinstance(image_path, Path):
            raise TypeError("image_path must be a pathlib.Path object.")
        self.image_path = image_path
        try:
            self.image = Image.open(image_path)
        except (FileNotFoundError, OSError):
            raise ValueError("Failed to load the image. Please provide a valid image file.")

    # Setter for image attribute
    def set_image(self, image: Image) -> None:
        if not isinstance(image, Image.Image):
            raise TypeError("image must be a PIL Image object.")
        self.image = image
    
    # Setter for localised_text attribute
    def set_localised_text(self, localised_text: List[str]) -> None:
        if not isinstance(localised_text, list):
            raise TypeError("localised_text must be a list object.")
        self.localised_text = localised_text
    
    # Setter for original_lang_code attribute
    def set_original_lang_code(self, original_lang_code: List[str]) -> None:
        if not isinstance(original_lang_code, List[str]):
            raise TypeError("original_lang_code must be a List[str].")
        self.original_lang_code = original_lang_code
    
    # Setter for translated_lang_code attribute
    def set_translated_lang_code(self, translated_lang_code: List[str]) -> None:
        if not isinstance(translated_lang_code, List[str]):
            raise TypeError("translated_lang_code must be a List[str].")
        self.translated_lang_code = translated_lang_code

    def get_language_name(self, lang_code: str) -> str:
        """
        Get the full name of the language corresponding to the given language code.
        
        Args:
            lang_code (str): Language code.
        
        Returns:
            str: Full name of the language.
        """
        
        return self.LANG_CODES_TO_NAMES.get(lang_code, None)

    def perform_ocr(self, output_folder: Path = None, original_lang_code: List[str] = None) -> None:
        """
        Perform OCR on the image to extract localized text.
        
        Args:
            output_folder (Path, optional): Path to save the annotated images. Defaults to None.
            original_lang_code (List[str], optional): List of language codes for recognition. Defaults to None.
        """
        output_folder = output_folder or self.image_path.parent if self.image_path else None
        original_lang_code = self.original_lang_code or ["en"]
        
        if self.image_path:
            self.localised_text = easy_ocr.text_inference(self.image_path, output_folder=output_folder,
                                                          language_code=original_lang_code, annotate=True)
        elif self.image:
            self.localised_text = easy_ocr.text_inference(self.image, output_folder=output_folder,
                                                          language_code=original_lang_code, annotate=True)
        else:
            raise ValueError("No image or image path provided for OCR.")

    def perform_translation(self, original_lang_code: str = None, translated_lang_code: str = None) -> None:
        """
        Perform translation of localized text.
        
        Args:
            original_lang_code (str, optional): Original language of the text. Defaults to None.
            translated_lang_code (str, optional): Target language for translation. Defaults to None.
        """
        original_lang_code = self.original_lang_code or original_lang_code or ["en"]
        translated_lang_code = self.translated_lang_code or translated_lang_code or ["zh"]

        original_language = self.get_language_name(original_lang_code[0]) or "English"
        translated_language = self.get_language_name(translated_lang_code[0]) or "Chinese"


        for i, (bbox, text) in enumerate(self.localised_text):
            translated_text = translate.translate_language(text=text, original_language=original_language,
                                                            translated_language=translated_language)
            self.localised_text[i] = (bbox, text, translated_text)

    def overlay_text(self, translated_lang_code:List[str] = None) -> None:
        """
        Overlay translated text onto the image.
        """
        translated_lang_code = self.translated_lang_code or translated_lang_code or ["en"]
        self.image = easy_ocr.overlay_text(self.image_path, self.localised_text, lang_code=translated_lang_code)


    def process_image(self, output_folder: Path = None, original_lang_code: List[str] = None,
                      translated_lang_code: List[str] = None) -> None:
        """
        Process the image by performing OCR, translation, and overlaying text.
        
        Args:
            output_folder (Path, optional): Path to save the annotated images. Defaults to None.
            original_lang_code (List[str], optional): Original language of the text. If self.original_lang_code is specified, that will be used, else Defaults to None.
            translated_lang_code (List[str], optional): Target language for translation. If self.translated_lang_code is specified, that will be used, else Defaults to None.Defaults to None.
        """
        output_folder = output_folder or self.image_path.parent if self.image_path else None
        original_lang_code = original_lang_code or self.original_lang_code
        translated_lang_code = translated_lang_code or self.translated_lang_code
        
        self.perform_ocr(output_folder, original_lang_code=original_lang_code)
        self.perform_translation(original_lang_code=original_lang_code, translated_lang_code=translated_lang_code)
        self.overlay_text(translated_lang_code=translated_lang_code)
    
    def save_image(self, output_path: Path) -> Path:
        """
        Save the modified image.
        
        Args:
            output_path (Path): Path to save the image.
        
        Returns:
            Path: Path of the saved image.
        """
        self.image.save(output_path)
        return output_path

if __name__ == "__main__":
    import os
    current_directory = Path.cwd()
    folder_dir = Path(r"C:\Users\alpha\OneDrive\Desktop\Life\NTU\FYP\FYP\images\Manga109_released_2023_12_07\images\AisazuNihaIrarenai\001.jpg")
    # folder_dir = current_directory / folder_dir
    output_folder = current_directory / "images" / "output" / "easyocr" / "slide"
    os.makedirs(output_folder, exist_ok=True)

    image = ImageObject(image_path=folder_dir, original_lang_code=["ja"], translated_lang_code=["en"])
    image.process_image()
    image.save_image(output_folder / f"translated_image_{99}.png")
    print("Text overlayed on image.")
