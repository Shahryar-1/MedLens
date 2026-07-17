import cv2
import numpy as np


class OCRVisualizer:
    """
    Draw OCR bounding boxes, text, and confidence.
    """

    @staticmethod
    def draw(image, results):
        output = image.copy()

        # If grayscale, convert to BGR so colored drawings are visible
        if len(output.shape) == 2:
            output = cv2.cvtColor(output, cv2.COLOR_GRAY2BGR)

        for box, text, confidence in results:

            points = np.array(box, dtype=np.int32)

            # Draw bounding box
            cv2.polylines(
                output,
                [points],
                isClosed=True,
                color=(0, 255, 0),
                thickness=2,
            )

            # Draw label
            label = f"{text} ({confidence:.2f})"

            x, y = points[0]

            cv2.putText(
                output,
                label,
                (x, max(y - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 0, 0),
                2,
            )

        return output