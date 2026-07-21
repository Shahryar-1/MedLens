class ROI:

    @staticmethod
    def extract(frame, x, y, width, height):
        """
        Extract Region of Interest (ROI) from an image.
        """

        return frame[y:y + height, x:x + width]