import pytesseract
from pdf2image import convert_from_path

class OCRProcessor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_text(self):
        # Convert PDF to images
        images = convert_from_path(self.pdf_path)
        text = ''
        for image in images:
            text += pytesseract.image_to_string(image) + '\n'
        return text

# Example usage:

# ocr_processor = OCRProcessor('path_to_your_pdf.pdf')
# extracted_text = ocr_processor.extract_text()
# print(extracted_text)
