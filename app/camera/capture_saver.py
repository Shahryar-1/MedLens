import cv2


class CaptureSaver:
    """
    Handles saving captured images
    and OCR results.
    """

    @staticmethod
    def save(
        frame,
        roi,
        gray,
        texts,
        image_counter,
    ):

        original_path = (
            f"data/captures/original_{image_counter}.jpg"
        )

        roi_path = (
            f"data/captures/roi_{image_counter}.jpg"
        )

        gray_path = (
            f"data/captures/gray_{image_counter}.jpg"
        )

        text_path = (
            f"data/captures/ocr_{image_counter}.txt"
        )

        cv2.imwrite(original_path, frame)
        cv2.imwrite(roi_path, roi)
        cv2.imwrite(gray_path, gray)

        with open(
            text_path,
            "w",
            encoding="utf-8",
        ) as file:

            if texts:
                file.write("\n".join(texts))
            else:
                file.write("No text detected.")

        print(f"✅ Saved: {original_path}")
        print(f"✅ Saved: {roi_path}")
        print(f"✅ Saved: {gray_path}")
        print(f"✅ Saved: {text_path}\n")