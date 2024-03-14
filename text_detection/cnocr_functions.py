from cnocr import CnOcr

img_fp = './docs/examples/huochepiao.jpeg'
ocr = CnOcr()  # Use default values for all parameters
out = ocr.ocr(img_fp)

# scene: For scene images, suitable for recognizing text in general photography. Models in this category start with scene-, such as the scene-densenet_lite_136-gru model.
# doc: For document images, suitable for recognizing text in regular document screenshots, like scanned book pages. Models in this category start with doc-, such as the doc-densenet_lite_136-gru model.
# number: Specifically for recognizing only numbers (able to recognize only the ten digits 0~9), suitable for scenarios like bank card numbers, ID numbers, etc. Models in this category start with number-, such as the number-densenet_lite_136-gru model.
# general: For general scenarios, suitable for images without a clear preference. Models in this category do not have a specific prefix and maintain the same naming convention as older versions, such as the densenet_lite_136-gru model.```
print(out)