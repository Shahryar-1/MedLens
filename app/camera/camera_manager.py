import cv2

from app.vision.roi import ROI
from app.config.camera_config import (
    ROI_X,
    ROI_Y,
    ROI_WIDTH,
    ROI_HEIGHT,
)
from app.vision.image_utils import print_pixel_info
from app.vision.preprocessing import ImagePreprocessor


class CameraManager:
    """
    Handles webcam operations.
    """

    def __init__(self, camera_index=0):
        self.camera = None
        self.camera_index = camera_index

    def open_camera(self):
        """Open the webcam."""

        self.camera = cv2.VideoCapture(self.camera_index)

        if not self.camera.isOpened():
            raise RuntimeError("Unable to open camera.")

        print("✅ Camera opened successfully.")

    def start_preview(self):
        """Start live camera preview."""

        if self.camera is None:
            raise RuntimeError("Camera is not opened.")

        print("Starting Camera Preview...")
        print("Press 'S' to save image.")
        print("Press 'Q' to quit.")

        frame_info_printed = False
        image_counter = 1

        while True:

            success, frame = self.camera.read()

            if not success:
                print("Failed to capture frame.")
                break

            # Print frame information once
            if not frame_info_printed:

                print("\n========== FRAME INFORMATION ==========")
                print(f"Type      : {type(frame)}")
                print(f"Shape     : {frame.shape}")
                print(f"Data Type : {frame.dtype}")
                print("=======================================\n")

                print_pixel_info(frame, 320, 240)

                frame_info_printed = True

            # -----------------------------
            # Extract ROI
            # -----------------------------

            roi = ROI.extract(
                frame,
                ROI_X,
                ROI_Y,
                ROI_WIDTH,
                ROI_HEIGHT,
            )

            # -----------------------------
            # Image Preprocessing
            # -----------------------------

            gray = ImagePreprocessor.convert_to_grayscale(roi)
            blur = ImagePreprocessor.gaussian_blur(gray)
            processed = ImagePreprocessor.binary_threshold(blur)

            # -----------------------------
            # Draw ROI
            # -----------------------------

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
                (ROI_X, ROI_Y - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 0, 0),
                2,
            )

            # -----------------------------
            # Display Windows
            # -----------------------------

            cv2.imshow("Original", frame)
            cv2.imshow("ROI", roi)
            cv2.imshow("Processed ROI", processed)

            key = cv2.waitKey(1) & 0xFF

            # -----------------------------
            # Save Images
            # -----------------------------

            if key == ord("s"):

                original_path = f"data/captures/original_{image_counter}.jpg"
                roi_path = f"data/captures/roi_{image_counter}.jpg"
                processed_path = f"data/captures/processed_{image_counter}.jpg"

                cv2.imwrite(original_path, frame)
                cv2.imwrite(roi_path, roi)
                cv2.imwrite(processed_path, processed)

                print(f"✅ Saved: {original_path}")
                print(f"✅ Saved: {roi_path}")
                print(f"✅ Saved: {processed_path}")

                image_counter += 1

            elif key == ord("q"):
                print("Closing Preview...")
                break

        self.release_camera()

    def capture_frame(self):
        """Capture one frame."""

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