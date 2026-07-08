from app.camera.camera_manager import CameraManager


def main():
    camera = CameraManager()

    camera.open_camera()

    camera.start_preview()


if __name__ == "__main__":
    main()