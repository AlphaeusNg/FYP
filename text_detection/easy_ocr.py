from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import easyocr
import torch
import math


def draw_bounding_boxes(image_path, bounding_boxes, output_path):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    for box in bounding_boxes:
        xmin, ymin, xmax, ymax = box
        # check if xmin < xmax and ymin < ymax
        if xmin > xmax:
            xmin, xmax = xmax, xmin
        if ymin > ymax:
            ymin, ymax = ymax, ymin
        draw.rectangle([xmin, ymin, xmax, ymax], outline="red", width=2)

    image.save(output_path)


def blurred_background_color(image, bbox):
    xmin, ymin = bbox[0][0], bbox[0][1]
    xmax, ymax = bbox[2][0], bbox[2][1]

    # Extract pixels within the specified range
    region = image.crop((xmin, ymin, xmax, ymax))

    # Convert the region to RGB mode
    region_rgb = region.convert("RGB")

    # Apply a blur filter to the region
    blurred_region = region_rgb.filter(ImageFilter.GaussianBlur(radius=5))

    # Convert the blurred region to RGB mode
    blurred_rgb_region = blurred_region.convert("RGB")

    # Calculate the sum of RGB values for each pixel in the blurred region
    total_r, total_g, total_b = 0, 0, 0
    num_pixels = 0
    for x in range(blurred_rgb_region.width):
        for y in range(blurred_rgb_region.height):
            r, g, b = blurred_rgb_region.getpixel((x, y))
            # Exclude black pixels from the calculation
            if r > 0 or g > 0 or b > 0:
                total_r += r
                total_g += g
                total_b += b
                num_pixels += 1

    # Calculate the average color of the blurred region
    if num_pixels > 0:
        blurred_avg_color = (
            total_r // num_pixels,
            total_g // num_pixels,
            total_b // num_pixels
        )
    else:
        # If no non-black pixels found, return white color as fallback
        blurred_avg_color = (255, 255, 255)

    return blurred_avg_color
    

# Define a function to overlay text on the image
def overlay_text(image_path, text_data):
    # Load the original image
    original_image = Image.open(image_path)

    # Create a copy of the original image for modification
    image = original_image.copy()
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()  # You can adjust the font as needed

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
        if luminance > 0.5:
            text_fill_color = (0, 0, 0)  # Use black text on light background
        else:
            text_fill_color = (255, 255, 255)  # Use white text on dark background

        # Calculate font size based on bounding box size
        bbox_width = xmax - xmin
        bbox_height = ymax - ymin
        text_length = len(translated_text)
        sqrt_text_length = 2/math.sqrt(text_length)
        font_size = max(min(bbox_width, bbox_height) * sqrt_text_length, 16)  # 16 is a minimum font size that's still readable
        font = ImageFont.truetype("arial.ttf", size=font_size)

        # Draw the translated text on top of the filled rectangle
        # Split text into multiple lines if it exceeds the bounding box width
        text_lines = []
        line = ""
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

    # Return the modified image
    return image


def text_inference(image_path: Path, output_folder: Path=None, 
                   language_code: list[str]=['ja'], annotate=True) -> list[tuple[str, float]]:
    gpu_available = torch.cuda.is_available()
    reader = easyocr.Reader(language_code, gpu=gpu_available)
    result = reader.readtext(image=str(image_path), paragraph=True, rotation_info=[0,90], 
                             x_ths=0.01, y_ths=0.01, slope_ths=0.01)
    bounding_boxes_list = []

    # Process the result
    for result_entry in result:
        # print(result_entry)
        xmin, ymin, = result_entry[0][0][0], result_entry[0][0][1]
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
    folder_dir = Path("images\Manga109_released_2023_12_07\images")
    folder_name = Path(r"AisazuNihaIrarenai")

    full_folder_dir = current_directory / folder_dir / folder_name
    output_folder = current_directory / "images" / "output" / "easyocr" / folder_name
    output_folder.mkdir(exist_ok=True)

    if full_folder_dir.is_dir():
        for count, file in enumerate(os.listdir(full_folder_dir)):
            text_inference(full_folder_dir.joinpath(file), output_folder)
    elif full_folder_dir.is_file():
        text_inference(full_folder_dir, output_folder)
        

    

    