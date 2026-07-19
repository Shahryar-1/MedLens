import re


class TextCleaner:
    """
    Cleans OCR output before further processing.
    """

    MIN_CONFIDENCE = 0.50
    MIN_LENGTH = 3

    @staticmethod
    def clean(results):

        cleaned_texts = []
        seen = set()

        for _, text, confidence in results:

            # Skip low-confidence detections
            if confidence < TextCleaner.MIN_CONFIDENCE:
                continue

            # Remove unwanted symbols
            text = re.sub(r"[^A-Za-z0-9\- ]", "", text)

            # Remove extra spaces
            text = text.strip()

            # Skip short text
            if len(text) < TextCleaner.MIN_LENGTH:
                continue

            # Remove duplicates (case-insensitive)
            key = text.lower()

            if key in seen:
                continue

            seen.add(key)
            cleaned_texts.append(text)

        return cleaned_texts