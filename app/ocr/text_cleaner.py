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

            if confidence < TextCleaner.MIN_CONFIDENCE:
                continue

            text = re.sub(r"[^A-Za-z0-9\- ]", "", text)

            text = text.strip()

            if len(text) < TextCleaner.MIN_LENGTH:
                continue

            key = text.lower()

            if key in seen:
                continue

            seen.add(key)
            cleaned_texts.append(text)

        return cleaned_texts