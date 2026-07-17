import cv2
from app.vision.ocr_visualizer import OCRVisualizer
from app.config.camera_config import (
    ROI_X,
    ROI_Y,
    ROI_WIDTH,
    ROI_HEIGHT,
)

from app.vision.roi import ROI
from app.vision.image_utils import print_pixel_info
from app.vision.preprocessing import ImagePreprocessor

from app.ocr.ocr_engine import OCREngine
from app.ocr.text_cleaner import TextCleaner


class CameraManager:
    """
    Handles webcam operations.

    Workflow:
    Camera → ROI → Grayscale → OCR → Save
    """

    def __init__(self, camera_index=0):
        self.camera = None
        self.camera_index = camera_index
        self.ocr = OCREngine()

    def open_camera(self):
        """Open webcam."""

        self.camera = cv2.VideoCapture(self.camera_index)

        if not self.camera.isOpened():
            raise RuntimeError("Unable to open camera.")

        print("✅ Camera opened successfully.")

    def start_preview(self):
        """Start live camera preview."""

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

            # ----------------------------------
            # Print Frame Information (Once)
            # ----------------------------------

            if not frame_info_printed:

                print("\n========== FRAME INFORMATION ==========")
                print(f"Type      : {type(frame)}")
                print(f"Shape     : {frame.shape}")
                print(f"Data Type : {frame.dtype}")
                print("=======================================\n")

                print_pixel_info(frame, 320, 240)

                frame_info_printed = True

            # ----------------------------------
            # Extract ROI
            # ----------------------------------

            roi = ROI.extract(
                frame,
                ROI_X,
                ROI_Y,
                ROI_WIDTH,
                ROI_HEIGHT,
            )

            # ----------------------------------
            # Preprocessing
            # ----------------------------------

            gray = ImagePreprocessor.convert_to_grayscale(roi)
            gray = cv2.resize(
                    gray,
                    None,
                    fx=2,
                    fy=2,
                    interpolation=cv2.INTER_CUBIC,
                    )
            # ----------------------------------
            # Draw UI
            # ----------------------------------

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

            # ----------------------------------
            # Show Windows
            # ----------------------------------

            cv2.imshow("Original", frame)
            cv2.imshow("ROI", roi)
            cv2.imshow("Gray ROI", gray)

            key = cv2.waitKey(1) & 0xFF

            # ----------------------------------
            # Scan Medicine
            # ----------------------------------

            if key == ord("s"):

                print("\n🔍 Scanning Medicine...\n")

                results = self.ocr.read_text(gray)
                
                visualized = OCRVisualizer.draw(gray, results)
                cv2.imshow(
                 "OCR Detection",
                  visualized
                    )

                texts = TextCleaner.clean(results)

                original_path = f"data/captures/original_{image_counter}.jpg"
                roi_path = f"data/captures/roi_{image_counter}.jpg"
                gray_path = f"data/captures/gray_{image_counter}.jpg"
                text_path = f"data/captures/ocr_{image_counter}.txt"

                cv2.imwrite(original_path, frame)
                cv2.imwrite(roi_path, roi)
                cv2.imwrite(gray_path, gray)

                with open(text_path, "w", encoding="utf-8") as file:
                    if texts:
                        file.write("\n".join(texts))
                    else:
                        file.write("No text detected.")

                print("========== OCR RESULT ==========")

                if texts:
                    for text in texts:
                        print(text)
                else:
                    print("No text detected.")

                print("================================\n")

                print(f"✅ Saved: {original_path}")
                print(f"✅ Saved: {roi_path}")
                print(f"✅ Saved: {gray_path}")
                print(f"✅ Saved: {text_path}\n")

                image_counter += 1

            elif key == ord("q"):
                print("Closing Preview...")
                break

        self.release_camera()

    def capture_frame(self):
        """Capture a single frame."""

        if self.camera is None:
            raise RuntimeError("Camera is not opened.")

        success, frame = self.camera.read()

        if not success:
            raise RuntimeError("Unable to capture frame.")

        return frame

    def release_camera(self):
        """Release camera resources."""

        if self.camera is not None:
            self.camera.release()
            self.camera = None

        cv2.destroyAllWindows()

        print("✅ Camera released successfully.")