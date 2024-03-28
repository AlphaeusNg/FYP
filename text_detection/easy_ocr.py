from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
import easyocr
import torch
import math
from typing import Tuple, List

def draw_bounding_boxes(image_path: Path, bounding_boxes: List[Tuple[int, int, int, int]], output_path: Path) -> None:
    """
    Draw bounding boxes on the given image and save the modified image.

    Args:
        image_path (Path): Path to the input image.
        bounding_boxes (List[Tuple[int, int, int, int]]): List of bounding boxes.
        output_path (Path): Path to save the modified image.
    """
    # Open image
    if image_path.suffix == ".png":
        image = Image.open(image_path).convert("RGBA")
    else:
        image = Image.open(image_path)

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Draw bounding boxes
    for box in bounding_boxes:
        xmin, ymin, xmax, ymax = box
        # Ensure xmin < xmax and ymin < ymax
        if xmin > xmax:
            xmin, xmax = xmax, xmin
        if ymin > ymax:
            ymin, ymax = ymax, ymin
        draw.rectangle([xmin, ymin, xmax, ymax], outline=(255, 0, 0), width=2)  # Red color outline

    # Save the modified image
    image.save(output_path)

def blurred_background_color(image: Image, bbox: Tuple[Tuple[int, int], Tuple[int, int]]) -> Tuple[int, int, int]:
    """
    Calculate the average color of the blurred background within the specified bounding box.

    Args:
        image (Image): Input image.
        bbox (Tuple[Tuple[int, int], Tuple[int, int]]): Bounding box coordinates.

    Returns:
        Tuple[int, int, int]: Average RGB color of the blurred background.
    """
    # Extract pixels within the specified range
    region = image.crop((bbox[0][0], bbox[0][1], bbox[2][0], bbox[2][1]))

    # Convert region to RGB mode and apply blur filter
    blurred_region = region.convert("RGB").filter(ImageFilter.GaussianBlur(radius=5))

    # Calculate average color of the blurred region
    total_r, total_g, total_b, num_pixels = 0, 0, 0, 0
    for x in range(blurred_region.width):
        for y in range(blurred_region.height):
            r, g, b = blurred_region.getpixel((x, y))
            if r > 0 or g > 0 or b > 0:  # Exclude black pixels
                total_r += r
                total_g += g
                total_b += b
                num_pixels += 1

    # Calculate average color
    if num_pixels > 0:
        return total_r // num_pixels, total_g // num_pixels, total_b // num_pixels
    else:
        return 255, 255, 255  # Fallback to white color


def convert_rgba_to_png(image: Image) -> Image:
    """
    Convert an RGBA image to PNG format.

    Args:
        image (Image): The input RGBA image.

    Returns:
        Image: The image converted to PNG format.
    """
    # Create a BytesIO object to hold the image data
    image_buffer = BytesIO()
    
    # Convert the image to PNG format and save it to the BytesIO buffer
    image.save(image_buffer, format="PNG")
    
    # Seek to the beginning of the buffer
    image_buffer.seek(0)
    
    # Open the image from the buffer and return it
    return Image.open(image_buffer)


def overlay_text(image_path: Path, text_data: List[Tuple[Tuple[int, int, int, int], float, str]], lang_code: list[str]) -> Image:
    """
    Overlay translated text on the image.

    Args:
        image_path (Path): Path to the input image.
        text_data (List[Tuple[Tuple[int, int, int, int], float, str]]): List of text data (bounding box, confidence, translated text).
        lang_code (str): Language code for selecting appropriate font.

    Returns:
        Image: Image with overlaid text.
    """
    # Load the original image
    if image_path.suffix == ".png":
        original_image = Image.open(image_path).convert("RGBA")
    else:
        original_image = Image.open(image_path)

    # Create a copy of the original image for modification
    image = original_image.copy()
    draw = ImageDraw.Draw(image)

    # Select font based on language code
    font_names_dict = {
        # Chinese
        "zh": ["simsun.ttc", "simhei.ttf", "msyh.ttc"],
        # Japanese
        "ja": ["msmincho.ttc", "meiryo.ttc", "msgothic.ttc"],
        # Korean
        "ko": ["malgun.ttf", "batang.ttc", "gulim.ttc"],
        # Thai
        "th": ["angsana.ttc", "loma.ttf", "garuda.ttf"],
        # Arabic
        "ar": ["amiri.ttf", "droidnaskh-regular.ttf", "kacstbook.ttf"],
        # Portuguese
        "pt": ["Arial Unicode.ttf", "DejaVuSans.ttf", "NotoSans-Regular.ttf"]
    }

    # Get the font name based on the language code, defaulting to Arial.ttf if not found
    font_name = font_names_dict.get(lang_code[0], ["arial.ttf"])[0]

    # Iterate over each bounding box and extract the mean RGB values
    for bbox, _, translated_text in text_data:
        # Extract coordinates from bounding box
        xmin, ymin = bbox[0][0], bbox[0][1]
        xmax, ymax = bbox[2][0], bbox[2][1]

        # Extract pixels within the specified range from the original image
        region = original_image.crop((xmin, ymin, xmax, ymax))

        # Calculate and draw a filled rectangle with the blurred background RGB color
        new_rgb = blurred_background_color(region, bbox)
        draw.rectangle([xmin, ymin, xmax, ymax], fill=new_rgb)

        # Calculate the luminance (brightness) of the background color
        luminance = (0.299 * new_rgb[0] + 0.587 * new_rgb[1] + 0.114 * new_rgb[2]) / 255
        text_fill_color = (0, 0, 0) if luminance > 0.5 else (255, 255, 255)

        # Calculate font size based on bounding box size
        bbox_width, bbox_height = xmax - xmin, ymax - ymin
        text_length = len(translated_text)
        if lang_code[0] == "zh":
            sqrt_text_length = 1/math.sqrt(text_length)
            font_size = max(min(bbox_width, bbox_height) * sqrt_text_length, 30)  # 30 is a minimum font size that's still readable
        else:
            sqrt_text_length = 2/math.sqrt(text_length)
            font_size = max(min(bbox_width, bbox_height) * sqrt_text_length, 16)  # 16 is a minimum font size that's still readable
        
        font = ImageFont.truetype(font_name, font_size)
        # Split text into multiple lines if it exceeds the bounding box width
        text_lines = []
        line = ""
        if lang_code[0] == "zh":
            for word in translated_text:
                # Check if adding the next word exceeds the bounding box width
                if draw.textlength(line + word, font=font) <= bbox_width:
                    line += word
                else:
                    text_lines.append(line)
                    line = word
        else:
            for word in translated_text.split():
                # Check if adding the next word exceeds the bounding box width
                if draw.textlength(line + word, font=font) <= bbox_width:
                    line += word + " "
                else:
                    text_lines.append(line.strip())
                    line = word + " "
        text_lines.append(line.strip())

        # Draw the text on multiple lines within the bounding box
        y_offset = ymin
        text_height = font_size
        for line in text_lines:
            # Draw the text on the image
            draw.text((xmin, y_offset), line, fill=text_fill_color, font=font)
            # Move to the next line
            y_offset += text_height
    return image

def text_inference(image_path: Path, output_folder: Path = None, language_code: List[str] = ['ja'], annotate: bool = True) -> List[Tuple[str, float]]:
    """
    Perform text detection and recognition on the input image using EasyOCR.

    Args:
        image_path (Path): Path to the input image.
        output_folder (Path, optional): Path to save the annotated images. Defaults to None.
        language_code (List[str], optional): List of language codes for recognition. Defaults to ['ja'].
        annotate (bool, optional): Whether to annotate the image with bounding boxes. Defaults to True.

    Returns:
        List[Tuple[str, float]]: A list of tuples containing the recognized text and confidence scores."""
    
    gpu_available = torch.cuda.is_available()
    reader = easyocr.Reader(language_code, gpu=gpu_available)
    result = reader.readtext(image=str(image_path), paragraph=True)
    bounding_boxes_list = []

    # Process the result
    for result_entry in result:
        xmin, ymin = result_entry[0][0][0], result_entry[0][0][1]
        xmax, ymax = result_entry[0][2][0], result_entry[0][2][1]
        bounding_boxes_list.append((xmin, ymin, xmax, ymax))

    # Draw bounding boxes on the image
    if output_folder is None:
        output_folder = image_path.parent
    output_image_path = output_folder / f"annotated_{image_path.name}"

    if annotate:
        draw_bounding_boxes(image_path, bounding_boxes_list, output_image_path)
        print(f"Bounding boxes drawn on: {output_image_path}")

    return result


if __name__ == "__main__":
    import os
    current_directory = Path.cwd()
    folder_dir = Path(r"images\Manga109_released_2023_12_07\images\AisazuNihaIrarenai\001.jpg")
    
    full_folder_dir = current_directory / folder_dir
    output_folder = current_directory / "images" / "output" / "easyocr" / "AisazuNihaIrarenai"
    output_folder.mkdir(exist_ok=True)
    lang_code = ["en"]
    if full_folder_dir.is_dir():
        for count, file in enumerate(os.listdir(full_folder_dir)):
            text_inference(full_folder_dir.joinpath(file), output_folder, lang_code)
    elif full_folder_dir.is_file():
        text_inference(full_folder_dir, output_folder, lang_code)
