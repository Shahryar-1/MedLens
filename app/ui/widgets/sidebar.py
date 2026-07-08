from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
)

from app.config import colors


class Sidebar(QWidget):
    """
    Sidebar navigation for MedLens.

    Responsibility:
    - Display navigation buttons.
    - Notify MainWindow when a button is clicked.
    """

    page_changed = Signal(str)

    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        self.setFixedWidth(220)

        self.setStyleSheet(
            f"""
            QWidget {{
                background-color: white;
            }}

            QLabel {{
                color: {colors.TEXT};
                font-size: 24px;
                font-weight: bold;
            }}

            QPushButton {{
                text-align: left;
                padding: 12px;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                color: {colors.TEXT};
            }}

            QPushButton:hover {{
                background-color: #EAF2FF;
            }}
            """
        )

        layout = QVBoxLayout()
        layout.setSpacing(12)

        title = QLabel("💙 MedLens")

        layout.addWidget(title)
        layout.addSpacing(20)

        self.dashboard_btn = QPushButton("🏠 Dashboard")
        self.scan_btn = QPushButton("📷 Scan Medicine")
        self.medicine_btn = QPushButton("💊 My Medicines")
        self.reminder_btn = QPushButton("🔔 Reminders")
        self.help_btn = QPushButton("❓ Help")
        self.settings_btn = QPushButton("⚙ Settings")

        layout.addWidget(self.dashboard_btn)
        layout.addWidget(self.scan_btn)
        layout.addWidget(self.medicine_btn)
        layout.addWidget(self.reminder_btn)
        layout.addWidget(self.help_btn)

        layout.addStretch()

        layout.addWidget(self.settings_btn)

        self.setLayout(layout)

        # Signals

        self.dashboard_btn.clicked.connect(
            lambda: self.page_changed.emit("dashboard")
        )

        self.scan_btn.clicked.connect(
            lambda: self.page_changed.emit("scan")
        )

        self.medicine_btn.clicked.connect(
            lambda: self.page_changed.emit("medicines")
        )

        self.reminder_btn.clicked.connect(
            lambda: self.page_changed.emit("reminders")
        )

        self.help_btn.clicked.connect(
            lambda: self.page_changed.emit("help")
        )

        self.settings_btn.clicked.connect(
            lambda: self.page_changed.emit("settings")
        )