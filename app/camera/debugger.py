class Debugger:
    """
    Handles all debug output for MedLens.
    """

    @staticmethod
    def print_frame_info(frame):

        print("\n========== FRAME INFORMATION ==========")
        print(f"Type      : {type(frame)}")
        print(f"Shape     : {frame.shape}")
        print(f"Data Type : {frame.dtype}")
        print("=======================================\n")

    @staticmethod
    def print_raw_ocr(results):

        print("========== RAW OCR ==========")

        if not results:
            print("No raw OCR results.")
            return

        for _, text, confidence in results:

            print(f"Text       : {text}")
            print(f"Confidence : {confidence:.3f}")
            print("----------------------------")

    @staticmethod
    def print_clean_text(texts):

        print("========== OCR RESULT ==========")

        if texts:

            for text in texts:
                print(text)

        else:

            print("No text detected.")

        print("================================\n")