import cv2


class ImagePreprocessor:
    """
    Image preprocessing utilities for MedLens.
    """

    @staticmethod
    def convert_to_grayscale(frame):
        """
        Convert a BGR image to grayscale.
        """
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def gaussian_blur(frame):
        """
        Reduce image noise.
        """
        return cv2.GaussianBlur(frame, (5, 5), 0)

    @staticmethod
    def binary_threshold(frame):
        """
        Convert grayscale image to binary.
        """
        _, threshold = cv2.threshold(
            frame,
            150,
            255,
            cv2.THRESH_BINARY
        )

        return threshold