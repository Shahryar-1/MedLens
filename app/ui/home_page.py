from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from app.config import colors


class HomePage(QWidget):
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
                font-size: 30px;
                font-weight: bold;
            }}

            QLabel#subtitle {{
                color: {colors.TEXT};
                font-size: 16px;
            }}

            QPushButton {{
                background-color: {colors.PRIMARY};
                color: white;
                font-size: 16px;
                padding: 12px;
                border-radius: 8px;
            }}

            QPushButton:hover {{
                background-color: #1565C0;
            }}
            """
        )

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        title = QLabel("MedLens")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("AI Medical Assistant")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)

        btn_scan = QPushButton("📷 Scan Medicine")
        btn_medicine = QPushButton("💊 My Medicines")
        btn_reminder = QPushButton("🔔 Reminders")
        btn_settings = QPushButton("⚙ Settings")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)

        layout.addWidget(btn_scan)
        layout.addWidget(btn_medicine)
        layout.addWidget(btn_reminder)
        layout.addWidget(btn_settings)

        self.setLayout(layout)