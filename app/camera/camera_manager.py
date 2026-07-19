import cv2

from app.config.camera_config import (
    ROI_X,
    ROI_Y,
    ROI_WIDTH,
    ROI_HEIGHT,
)

from app.ocr.ocr_engine import OCREngine
from app.ocr.text_cleaner import TextCleaner
from app.vision.lighting_detector import LightingDetector
from app.vision.blur_detector import BlurDetector
from app.vision.image_utils import print_pixel_info
from app.vision.ocr_visualizer import OCRVisualizer
from app.vision.preprocessing import ImagePreprocessor
from app.vision.roi import ROI


class CameraManager:
    """
    Handles all webcam operations.

    Pipeline:

    Camera
        ↓
    ROI Extraction
        ↓
    Image Preprocessing
        ↓
    Blur Detection
        ↓
    OCR
        ↓
    Text Cleaning
        ↓
    Save Results
    """

    def __init__(self, camera_index=0):

        self.camera = None
        self.camera_index = camera_index
        self.ocr = OCREngine()

    # --------------------------------------------------
    # Camera
    # --------------------------------------------------

    def open_camera(self):

        self.camera = cv2.VideoCapture(self.camera_index)

        if not self.camera.isOpened():
            raise RuntimeError("Unable to open camera.")

        print("✅ Camera opened successfully.")

    # --------------------------------------------------
    # Preview
    # --------------------------------------------------

    def start_preview(self):

        if self.camera is None:
            raise RuntimeError("Camera is not opened.")

        print("Starting Camera Preview...")
        print("Press 'S' to Scan Medicine.")
        print("Press 'Q' to Quit.\n")

        frame_info_printed = False
        image_counter = 1

        while True:

            success, frame = self.camera.read()

            if not success:
                print("Failed to capture frame.")
                break

            if not frame_info_printed:

                print("\n========== FRAME INFORMATION ==========")
                print(f"Type      : {type(frame)}")
                print(f"Shape     : {frame.shape}")
                print(f"Data Type : {frame.dtype}")
                print("=======================================\n")

                print_pixel_info(frame, 320, 240)

                frame_info_printed = True

            roi = ROI.extract(
                frame,
                ROI_X,
                ROI_Y,
                ROI_WIDTH,
                ROI_HEIGHT,
            )

            gray = ImagePreprocessor.convert_to_grayscale(roi)
            
            gray = cv2.resize(
                gray,
                None,
                fx=2,
                fy=2,
                interpolation=cv2.INTER_CUBIC,
            )

            is_blurry, blur_score = BlurDetector.is_blurry(gray)

            self.draw_interface(frame, blur_score, is_blurry)

            cv2.imshow("Original", frame)
            cv2.imshow("ROI", roi)
            cv2.imshow("Gray ROI", gray)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("s"):

                if is_blurry:

                    print("\n⚠ Image is blurry.")
                    print(f"Sharpness Score : {blur_score:.2f}")
                    print("Hold camera steady and try again.\n")

                    continue

                self.scan_medicine(
                    frame,
                    roi,
                    gray,
                    image_counter,
                )

                image_counter += 1

            elif key == ord("q"):
                print("Closing Preview...")
                break

        self.release_camera()

    # --------------------------------------------------
    # Draw UI
    # --------------------------------------------------

    def draw_interface(
        self,
        frame,
        blur_score,
        is_blurry,
    ):

        cv2.rectangle(
            frame,
            (ROI_X, ROI_Y),
            (ROI_X + ROI_WIDTH, ROI_Y + ROI_HEIGHT),
            (0, 255, 0),
            2,
        )

        cv2.putText(
            frame,
            "MedLens Camera",
            (ROI_X, ROI_Y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 0, 0),
            2,
        )

        cv2.putText(
            frame,
            f"Sharpness : {blur_score:.0f}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2,
        )

        if is_blurry:

            cv2.putText(
                frame,
                "Hold Camera Steady",
                (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2,
            )

    # --------------------------------------------------
    # OCR
    # --------------------------------------------------

    def scan_medicine(
        self,
        frame,
        roi,
        gray,
        image_counter,
    ):

        print("\n🔍 Scanning Medicine...\n")

        results = self.ocr.read_text(gray)

        texts = TextCleaner.clean(results)

        visualized = OCRVisualizer.draw(gray, results)

        cv2.imshow(
            "OCR Detection",
            visualized,
        )

        self.print_raw_results(results)

        self.print_clean_results(texts)

        self.save_results(
            frame,
            roi,
            gray,
            texts,
            image_counter,
        )

    # --------------------------------------------------
    # Debug
    # --------------------------------------------------

    def print_raw_results(self, results):

        print("========== RAW OCR ==========")

        for _, text, confidence in results:

            print(f"Text       : {text}")
            print(f"Confidence : {confidence:.3f}")
            print("----------------------------")

    def print_clean_results(self, texts):

        print("========== OCR RESULT ==========")

        if texts:

            for text in texts:
                print(text)

        else:

            print("No text detected.")

        print("================================\n")

    # --------------------------------------------------
    # Save
    # --------------------------------------------------

    def save_results(
        self,
        frame,
        roi,
        gray,
        texts,
        image_counter,
    ):

        original_path = (
            f"data/captures/original_{image_counter}.jpg"
        )

        roi_path = (
            f"data/captures/roi_{image_counter}.jpg"
        )

        gray_path = (
            f"data/captures/gray_{image_counter}.jpg"
        )

        text_path = (
            f"data/captures/ocr_{image_counter}.txt"
        )

        cv2.imwrite(original_path, frame)
        cv2.imwrite(roi_path, roi)
        cv2.imwrite(gray_path, gray)

        with open(
            text_path,
            "w",
            encoding="utf-8",
        ) as file:

            if texts:

                file.write("\n".join(texts))

            else:

                file.write("No text detected.")

        print(f"✅ Saved: {original_path}")
        print(f"✅ Saved: {roi_path}")
        print(f"✅ Saved: {gray_path}")
        print(f"✅ Saved: {text_path}\n")

    # --------------------------------------------------
    # Capture
    # --------------------------------------------------

    def capture_frame(self):

        if self.camera is None:
            raise RuntimeError("Camera is not opened.")

        success, frame = self.camera.read()

        if not success:
            raise RuntimeError("Unable to capture frame.")

        return frame

    # --------------------------------------------------
    # Release
    # --------------------------------------------------

    def release_camera(self):

        if self.camera is not None:

            self.camera.release()
            self.camera = None

        cv2.destroyAllWindows()

        print("✅ Camera released successfully.")