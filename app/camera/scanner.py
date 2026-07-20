import cv2

from app.ocr.ocr_engine import OCREngine
from app.ocr.text_cleaner import TextCleaner
from app.vision.ocr_visualizer import OCRVisualizer

from app.camera.debugger import Debugger
from app.camera.capture_saver import CaptureSaver


class Scanner:
    """
    Handles the complete OCR scanning pipeline.
    """

    def __init__(self):
        self.ocr = OCREngine()

    def scan(
        self,
        frame,
        roi,
        gray,
        image_counter,
    ):

        print("\n🔍 Scanning Medicine...\n")

        # OCR
        results = self.ocr.read_text(gray)

        # Clean Text
        texts = TextCleaner.clean(results)

        # Visualization
        visualized = OCRVisualizer.draw(gray, results)

        cv2.imshow(
            "OCR Detection",
            visualized,
        )

        # Debug
        Debugger.print_raw_ocr(results)
        Debugger.print_clean_text(texts)

        # Save
        CaptureSaver.save(
            frame,
            roi,
            gray,
            texts,
            image_counter,
        )