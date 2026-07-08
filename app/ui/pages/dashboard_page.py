from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from app.config import colors


class DashboardPage(QWidget):
    """
    Dashboard page of MedLens.

    Responsibilities:
    - Welcome the user.
    - Display the primary action (Scan Medicine).
    - Provide a clean landing page.
    """

    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(
            f"""
            QWidget {{
                background-color: {colors.BACKGROUND};
            }}

            QLabel#title {{
                color: {colors.TEXT};
                font-size: 34px;
                font-weight: bold;
            }}

            QLabel#subtitle {{
                color: {colors.TEXT};
                font-size: 18px;
            }}

            QPushButton {{
                background-color: {colors.PRIMARY};
                color: white;
                font-size: 18px;
                padding: 14px;
                border-radius: 12px;
            }}

            QPushButton:hover {{
                background-color: #1565C0;
            }}
            """
        )

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        title = QLabel("Welcome to MedLens")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Your AI Medical Assistant")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)

        self.scan_button = QPushButton("📷 Scan Medicine")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addWidget(self.scan_button)

        self.setLayout(layout)