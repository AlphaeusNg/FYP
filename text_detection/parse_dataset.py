import os
import xml.etree.ElementTree as ET

def process_xml_files(source_dir, destination_dir):
    # Ensure the destination directory exists
    os.makedirs(destination_dir, exist_ok=True)

    # Iterate through each file in the source directory
    for filename in os.listdir(source_dir):
        if filename.endswith('.xml'):  # Check if the file is an XML file
            source_path = os.path.join(source_dir, filename)
            tree = ET.parse(source_path)
            root = tree.getroot()
            
            # Create a dictionary to store information for each page
            pages_info = {}

            # Find all pages and their text elements
            for page in root.findall('.//pages/page'):
                page_index = page.get('index')
                page_info = {'text': []}
                for text in page.findall('.//text'):
                    text_info = {
                        'id': text.get('id'),
                        'xmin': text.get('xmin'),
                        'ymin': text.get('ymin'),
                        'xmax': text.get('xmax'),
                        'ymax': text.get('ymax'),
                        'text': text.text.strip() if text.text else ''
                    }
                    page_info['text'].append(text_info)
                pages_info[page_index] = page_info
            
            # Write information for each page to a new XML file in the destination directory
            destination_path = os.path.join(destination_dir, filename)
            with open(destination_path, 'w', encoding='utf-8') as f:
                f.write('<text_info>\n')
                for page_index, page_info in pages_info.items():
                    f.write(f'  <page index="{page_index}">\n')
                    for text_info in page_info['text']:
                        f.write('    <text>\n')
                        f.write(f'      <id>{text_info["id"]}</id>\n')
                        f.write(f'      <xmin>{text_info["xmin"]}</xmin>\n')
                        f.write(f'      <ymin>{text_info["ymin"]}</ymin>\n')
                        f.write(f'      <xmax>{text_info["xmax"]}</xmax>\n')
                        f.write(f'      <ymax>{text_info["ymax"]}</ymax>\n')
                        f.write(f'      <text>{text_info["text"]}</text>\n')
                        f.write('    </text>\n')
                    f.write('  </page>\n')
                f.write('</text_info>\n')

            print(f'Processed: {filename}')

    print('All XML files processed.')

def main():
    source_dir = r'images\Manga109_released_2023_12_07\annotations.v2020.12.18'
    destination_dir = r'images\Manga109_released_2023_12_07\v2020_cleaned_annotations'
    process_xml_files(source_dir, destination_dir)

if __name__ == "__main__":
    main()
