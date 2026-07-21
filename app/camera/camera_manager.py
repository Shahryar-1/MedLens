import cv2

from app.config.camera_config import (
    ROI_X,
    ROI_Y,
    ROI_WIDTH,
    ROI_HEIGHT,
)

from app.camera.overlay import Overlay
from app.camera.scanner import Scanner
from app.camera.debugger import Debugger
from app.camera.quality_checker import QualityChecker

from app.vision.image_utils import print_pixel_info
from app.vision.preprocessing import ImagePreprocessor
from app.vision.roi import ROI


class CameraManager:
    """
    Handles webcam operations.

    Pipeline:

    Camera
        ↓
    ROI Extraction
        ↓
    Image Preprocessing
        ↓
    Quality Check
        ↓
    UI Overlay
        ↓
    OCR Scanner
    """

    def __init__(self, camera_index=0):

        self.camera = None
        self.camera_index = camera_index
        self.scanner = Scanner()

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

                Debugger.print_frame_info(frame)
                print_pixel_info(frame, 320, 240)

                frame_info_printed = True

            # ----------------------------------
            # ROI
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
            # Image Quality
            # ----------------------------------

            quality = QualityChecker.check(gray)

            # ----------------------------------
            # Overlay
            # ----------------------------------

            Overlay.draw(
                frame,
                quality["blur_score"],
                quality["brightness"],
                quality["is_blurry"],
                quality["lighting_status"],
            )

            # ----------------------------------
            # Display
            # ----------------------------------

            cv2.imshow("Original", frame)
            cv2.imshow("ROI", roi)
            cv2.imshow("Gray ROI", gray)

            key = cv2.waitKey(1) & 0xFF

            # ----------------------------------
            # Scan
            # ----------------------------------

            if key == ord("s"):

                if quality["is_blurry"]:

                    print("\n⚠ Image is blurry.")
                    print(
                        f"Sharpness Score : {quality['blur_score']:.2f}"
                    )
                    print("Hold camera steady and try again.\n")

                    continue

                if quality["lighting_status"] != "good":

                    print("\n⚠ Lighting is not suitable.")
                    print(
                        f"Brightness : {quality['brightness']:.2f}"
                    )

                    continue

                self.scanner.scan(
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