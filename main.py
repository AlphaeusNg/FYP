from pdf_to_png_converter import convert_image_path
from PIL import Image, ImageDraw
import os
import easyocr
import main_paddleocr as p_ocr


def draw_bounding_boxes(image_path, bounding_boxes, output_path):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    for box in bounding_boxes:
        # Assuming the bounding box is a tuple (x1, y1, x2, y2)
        x1, y1, x2, y2 = box
        draw.rectangle([x1, y1, x2, y2], outline="red", width=2)

    image.save(output_path)

image_path = 'images/Tsuihou Sareta Tenshou Juu Kishi wa game Chishiki de Musou Suru Chapter 64 Raw - Rawkuma_removed (1)_removed.pdf'
output_folder = "images/output"

png_image_paths = convert_image_path(image_path=image_path, output_folder=output_folder)

# easyocr
# reader = easyocr.Reader(['ja'], gpu=True)  # This needs to run only once to load the model into memory
#
# for png_image_path in png_image_paths:
#     result = reader.readtext(png_image_path)
#     print(result)
#
#     # Extract bounding box coordinates from the result
#     bounding_boxes = [(result_entry[0][0][0], result_entry[0][0][1], result_entry[0][2][0], result_entry[0][2][1])
#                        for result_entry in
#                        result]
#
#     # Draw bounding boxes on the image
#     output_image_path = f"{output_folder}/annotated_{os.path.basename(png_image_path)}"
#     draw_bounding_boxes(png_image_path, bounding_boxes, output_image_path)
#
#     print(f"Bounding boxes drawn on: {output_image_path}")

# paddleocr
for png_image_path in png_image_paths:
    output_image_path = f"{output_folder}/annotated_{os.path.basename(png_image_path)}"
    p_ocr.inference(png_image_path, output_image_path)