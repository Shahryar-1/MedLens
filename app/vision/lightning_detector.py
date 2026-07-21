import cv2
import numpy as np


class LightingDetector:
    """
    Detect whether an image is too dark,
    well exposed, or too bright.
    """

    DARK_THRESHOLD = 60
    BRIGHT_THRESHOLD = 190

    @staticmethod
    def analyze(gray):

        brightness = np.mean(gray)

        if brightness < LightingDetector.DARK_THRESHOLD:
            return "dark", brightness

        if brightness > LightingDetector.BRIGHT_THRESHOLD:
            return "bright", brightness

        return "good", brightness