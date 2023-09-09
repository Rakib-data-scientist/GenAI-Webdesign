from typing import List, Dict
import easyocr


class OCRProcessor:
    """
    A processor class that utilizes EasyOCR to extract textual data from images.
    """
    def __init__(self):
        self.reader = easyocr.Reader(['en'])

    def extract_layout(self, img_path: str) -> List[Dict[str, List[int]]]:
        """
        Extracts textual layout from the given image path.

        :param img_path: The path to the image file.
        :return: A list of dictionaries containing textual content and their respective coordinates.
        """
        results = self.reader.readtext(img_path)
        output = [{item[1]: [coord for sublist in item[0] for coord in sublist]} for item in results]
        
        return output


# Usage example:
# if __name__ == "__main__":
#     processor = OCRProcessor()
#     layout = processor.extract_layout("path_to_your_image.jpg")
#     print(layout)
