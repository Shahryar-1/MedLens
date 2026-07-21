import cv2

from app.config.camera_config import (
    ROI_X,
    ROI_Y,
    ROI_WIDTH,
    ROI_HEIGHT,
)


class Overlay:
    """
    Draw all UI elements on the camera preview.
    """

    @staticmethod
    def draw(
        frame,
        blur_score,
        brightness,
        is_blurry,
        lighting_status,
    ):

        # ROI Rectangle
        cv2.rectangle(
            frame,
            (ROI_X, ROI_Y),
            (ROI_X + ROI_WIDTH, ROI_Y + ROI_HEIGHT),
            (0, 255, 0),
            2,
        )

        # Title
        cv2.putText(
            frame,
            "MedLens Camera",
            (ROI_X, ROI_Y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 0, 0),
            2,
        )

        # Sharpness
        cv2.putText(
            frame,
            f"Sharpness : {blur_score:.0f}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2,
        )

        # Brightness
        cv2.putText(
            frame,
            f"Brightness : {brightness:.0f}",
            (20, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2,
        )

        # Blur Warning
        if is_blurry:

            cv2.putText(
                frame,
                "Hold Camera Steady",
                (20, 95),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2,
            )

        # Lighting Warning
        if lighting_status == "dark":

            cv2.putText(
                frame,
                "Increase Lighting",
                (20, 125),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2,
            )

        elif lighting_status == "bright":

            cv2.putText(
                frame,
                "Reduce Glare",
                (20, 125),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2,
            )