import cv2
import os
import logging
from paddleocr import PaddleOCR

# Unwanted logs disable karne ke liye
logging.getLogger("ppocr").setLevel(logging.ERROR)

class VisionEngine:
    def __init__(self):
        # Handwritten table ke liye optimized settings
        self.ocr_engine = PaddleOCR(use_angle_cls=True, lang="en")

    def extract_raw_text(self, image_path):
        try:
            if not os.path.exists(image_path): return ""
            
            # PaddleOCR call
            result = self.ocr_engine.ocr(image_path)
            
            if not result or not result[0]: return ""

            # Bikhre hue text ko join karke ek string banana
            full_text = []
            for line in result[0]:
                if line and len(line) > 1:
                    full_text.append(line[1][0])
            
            return " ".join(full_text)
        except Exception as e:
            print(f"OCR Error: {e}")
            return ""

vision_engine = VisionEngine()