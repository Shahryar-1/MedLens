from PySide6.QtWidgets import QMainWindow

from app.ui.home_page import HomePage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MedLens")
        self.resize(1000, 650)

        self.home_page = HomePage()
        self.setCentralWidget(self.home_page)