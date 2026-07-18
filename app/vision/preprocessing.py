from email.mime import image

import cv2
import numpy as np

class ImagePreprocessor:
    """
    Image preprocessing utilities for MedLens.
    """

    @staticmethod
    def convert_to_grayscale(image):
        """Convert BGR image to grayscale."""
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def gaussian_blur(image, kernel_size=(5, 5)):
        """Reduce image noise."""
        return cv2.GaussianBlur(image, kernel_size, 0)

    @staticmethod
    def apply_clahe(image, clip_limit=2.0, tile_grid_size=(8, 8)):
        """
        Improve local contrast using CLAHE.
        """
        clahe = cv2.createCLAHE(
            clipLimit=clip_limit,
            tileGridSize=tile_grid_size,
        )

        return clahe.apply(image)

    @staticmethod
    def binary_threshold(image, threshold=150):
        """Apply binary threshold."""
        _, binary = cv2.threshold(
            image,
            threshold,
            255,
            cv2.THRESH_BINARY,
        )

        return binary
    
    @staticmethod
    def sharpen(image):
        """
        Sharpen image to improve OCR.
        """

        kernel = [
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0],
        ]

        kernel = np.array(kernel)

        return cv2.filter2D(
        image,
            -1,
            kernel,
        )