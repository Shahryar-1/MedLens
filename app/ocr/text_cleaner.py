class TextCleaner:

    @staticmethod
    def clean(results):

        texts = []

        for _, text, _ in results:
            texts.append(text)

        return texts