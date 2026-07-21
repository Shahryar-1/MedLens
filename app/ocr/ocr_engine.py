import easyocr


class OCREngine:
    """
    Handles all OCR operations.
    """

    def __init__(self, languages=None):

        if languages is None:
            languages = ["en"]

        self.reader = easyocr.Reader(languages)

    def read_text(self, image):
        """
        Perform OCR on an image.

        Parameters
        ----------
        image : numpy.ndarray

        Returns
        -------
        list
        """

        return self.reader.readtext(image)