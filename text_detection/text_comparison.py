from parse_dataset import parse_xml
from difflib import SequenceMatcher
import csv, os


def boxes_overlap(bbox1, bbox2):
    """
    Check if two bounding boxes overlap.
    Bounding box format: {'xmin': x1, 'ymin': y1, 'xmax': x2, 'ymax': y2}
    """
    # Check if bbox1 is to the right of bbox2
    if bbox1['xmin'] > bbox2['xmax'] or bbox2['xmin'] > bbox1['xmax']:
        return False

    # Check if bbox1 is below bbox2
    if bbox1['ymin'] > bbox2['ymax'] or bbox2['ymin'] > bbox1['ymax']:
        return False

    # Bounding boxes overlap
    return True


def compare_and_save_results(xml_data, ocr_data, output_file):
    """
    Compare text bounding boxes and save results.
    """
    with open(output_file, 'a', newline='') as csvfile:
        fieldnames = ['xml_bbox', 'ocr_bbox', 'xml_text', 'ocr_text', 'similarity_score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        for xml_bbox in xml_data:
            for ocr_bbox in ocr_data:
                # Compare bounding boxes for overlap
                if boxes_overlap(xml_bbox, ocr_bbox):
                    # Compute similarity between text content
                    similarity_score = compute_similarity(xml_bbox['text'], ocr_bbox['text'])

                    # Save the results
                    writer.writerow({
                        'xml_bbox': xml_bbox,
                        'ocr_bbox': ocr_bbox,
                        'xml_text': xml_bbox['text'],
                        'ocr_text': ocr_bbox['text'],
                        'similarity_score': similarity_score
                    })


def compute_similarity(text1, text2):
    """
    Compute similarity between two text strings.
    Returns a similarity score between 0 and 1.
    """
    return SequenceMatcher(None, text1, text2).ratio()


def main():
    xml_dir = 'path/to/xml/files'
    ocr_dir = 'path/to/images'
    output_file = 'results.csv'

    # Iterate through XML files
    for xml_file in os.listdir(xml_dir):
        if xml_file.endswith('.xml'):
            # Parse XML file
            xml_data = parse_xml(os.path.join(xml_dir, xml_file))

            # Find corresponding OCR data
            image_file = os.path.join(ocr_dir, xml_file.replace('.xml', '.jpg'))
            ocr_data = detect_text(image_file)

            # Compare and save results
            compare_and_save_results(xml_data, ocr_data, output_file)

    print('All comparisons done. Results saved.')

if __name__ == "__main__":
    main()