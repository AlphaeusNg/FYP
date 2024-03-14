from pathlib import Path
from typing import Union
from PIL import Image, ImageDraw
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


def text_inference(image_path: Union[Path, str], output_folder: Union[Path, str]) -> None:
    gpu_available = torch.cuda.is_available()
    reader = easyocr.Reader(['ja'], gpu=gpu_available)  # This needs to run only once to load the model into memory
    result = reader.readtext(str(image_path))
    print(result)

    # Extract bounding box coordinates from the result
    bounding_boxes = [(result_entry[0][0][0], result_entry[0][0][1], result_entry[0][2][0], result_entry[0][2][1])
                      for result_entry in
                      result]

    # Draw bounding boxes on the image
    output_image_path = output_folder / f"annotated_{image_path.name}"
    draw_bounding_boxes(image_path, bounding_boxes, output_image_path)
    print(f"Bounding boxes drawn on: {output_image_path}")

if __name__ == "__main__":
    current_directory = Path.cwd()
    image_path = current_directory / "images" / "Tsuihou Sareta Tenshou Juu Kishi wa game Chishiki de Musou Suru Chapter 64 Raw - Rawkuma" / "Tsuihou Sareta Tenshou Juu Kishi wa game Chishiki de Musou Suru Chapter 64 Raw - Rawkuma-03.png"
    output_folder = current_directory / "images" / "output" / "easyocr"
    text_inference(image_path, output_folder)
    

    

    