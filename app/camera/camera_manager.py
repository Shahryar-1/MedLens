import cv2


class CameraManager:
    """
    CameraManager is responsible for:
    - Opening the webcam
    - Reading frames
    - Displaying live preview
    - Releasing the camera safely
    """

    def __init__(self, camera_index=0):
        """
        Initialize the camera manager.

        Parameters:
            camera_index (int): Camera device index.
                                0 = Default webcam
                                1 = External webcam (if available)
        """
        self.camera = None
        self.camera_index = camera_index

    def open_camera(self):
        """
        Open the camera.
        """
        self.camera = cv2.VideoCapture(self.camera_index)

        if not self.camera.isOpened():
            raise RuntimeError("Unable to open camera.")

        print("✅ Camera opened successfully.")

    def start_preview(self):
        """
        Display live camera feed.
        Press 'q' to exit.
        """

        if self.camera is None:
            raise RuntimeError("Camera is not opened. Call open_camera() first.")

        print("Starting live preview...")
        print("Press 'Q' to exit.")

        while True:

            success, frame = self.camera.read()

            if not success:
                print("Failed to capture frame.")
                break

            cv2.imshow("MedLens Camera Preview", frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                print("Closing camera preview...")
                break

        self.release_camera()

    def capture_frame(self):
        """
        Capture a single frame.

        Returns:
            frame (numpy.ndarray): Captured image.
        """

        if self.camera is None:
            raise RuntimeError("Camera is not opened.")

        success, frame = self.camera.read()

        if not success:
            raise RuntimeError("Unable to capture frame.")

        return frame

    def release_camera(self):
        """
        Release camera resources safely.
        """

        if self.camera is not None:
            self.camera.release()
            self.camera = None

        cv2.destroyAllWindows()

        print("✅ Camera released successfully.")