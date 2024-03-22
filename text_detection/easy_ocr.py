from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import easyocr
import torch


def draw_bounding_boxes(image_path, bounding_boxes, output_path):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    for box in bounding_boxes:
        # Assuming the bounding box is a tuple (x1, y1, x2, y2)
        x1, y1, x2, y2 = box
        draw.rectangle([x1, y1, x2, y2], outline="red", width=2)

    image.save(output_path)


# Define a function to overlay text on the image
def overlay_text(image_path, text_data):
    # Open the image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    
    # Load a font
    font = ImageFont.load_default()

    # Overlay translated text onto the image
    for bbox, original_text, translated_text in text_data:
        # Extract coordinates from bounding box
        x_min, y_min, x_max, y_max = bbox

        # Find the rgb pixel value within the bbox area and determine the average colour
        pixel_values = list(image.getdata())
        pixel_values = pixel_values[x_min:x_max, y_min:y_max]
        average_color = pixel_values.mean(axis=0)
        # Draw the translated text
        draw.text((x_min, y_min), translated_text, fill=average_color, font=font)

    # Save or return the modified image
    image.save(image_path)
    return image


def text_inference(image_path: Path, output_folder: Path=None, 
                   language_code: list[str]=['ja'], annotate=True) -> list[tuple[str, float]]:
    gpu_available = torch.cuda.is_available()
    reader = easyocr.Reader(language_code, gpu=gpu_available)
    result = reader.readtext(image=str(image_path), paragraph=True, rotation_info=[90])
    bounding_boxes_list = []

    # Process the result
    for result_entry in result:
        print(result_entry)
        x1, y1, = result_entry[0][0][0], result_entry[0][0][1]
        x2, y2 = result_entry[0][2][0], result_entry[0][2][1]
        bounding_boxes_list.append((x1, y1, x2, y2))

    # Draw bounding boxes on the image
    if output_folder is None:
        output_folder = image_path.parent
    output_image_path = output_folder / f"annotated_{image_path.name}"

    if annotate:
        draw_bounding_boxes(image_path, bounding_boxes_list, output_image_path)
        print(f"Bounding boxes drawn on: {output_image_path}")

    return result

if __name__ == "__main__":
    current_directory = Path.cwd()
    image_path = current_directory / "images" / "Tsuihou Sareta Tenshou Juu Kishi wa game Chishiki de Musou Suru Chapter 64 Raw - Rawkuma" / "Tsuihou Sareta Tenshou Juu Kishi wa game Chishiki de Musou Suru Chapter 64 Raw - Rawkuma-03.png"
    output_folder = current_directory / "images" / "output" / "easyocr"
    text_inference(image_path, output_folder)
    

    

    