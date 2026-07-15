from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QHBoxLayout,
)

from app.config import colors


class BottomNavigation(QWidget):
    """
    Bottom navigation for MedLens.
    """

    page_changed = Signal(int)

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):

        self.setFixedHeight(70)

        self.setStyleSheet(f"""
            QWidget {{
                background: white;
                border-top: 1px solid #DADADA;
            }}

            QPushButton {{
                border: none;
                background: transparent;
                color: {colors.TEXT};
                font-size: 14px;
                font-weight: 600;
                padding: 10px;
            }}

            QPushButton:hover {{
                color: {colors.PRIMARY};
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 5, 15, 5)
        layout.setSpacing(20)

        pages = [
            ("🏠\nHome", 0),
            ("📜\nHistory", 1),
            ("🔔\nReminder", 2),
            ("⚙️\nSettings", 3),
        ]

        for text, index in pages:
            button = QPushButton(text)
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(
                lambda _, i=index: self.page_changed.emit(i)
            )
            layout.addWidget(button)