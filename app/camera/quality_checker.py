from app.vision.blur_detector import BlurDetector
from app.vision.lightning_detector import LightingDetector


class QualityChecker:
    """
    Checks image quality before OCR.

    - Blur
    - Lighting
    """

    @staticmethod
    def check(gray):

        is_blurry, blur_score = BlurDetector.is_blurry(gray)

        lighting_status, brightness = LightingDetector.analyze(gray)

        return {
            "is_blurry": is_blurry,
            "blur_score": blur_score,
            "lighting_status": lighting_status,
            "brightness": brightness,
        }