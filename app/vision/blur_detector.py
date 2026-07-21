import cv2


class BlurDetector:
    """
    Detect whether an image is blurry using the
    Variance of Laplacian method.
    """

    BLUR_THRESHOLD = 120

    @staticmethod
    def is_blurry(image):

        score = cv2.Laplacian(
            image,
            cv2.CV_64F
        ).var()

        return score < BlurDetector.BLUR_THRESHOLD, score