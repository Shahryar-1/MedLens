from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from app.config import colors
from app.ui.widgets.feature_card import FeatureCard


class DashboardPage(QWidget):
    """Home page of MedLens."""

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet(f"""
            QWidget {{
                background: {colors.BACKGROUND};
            }}

            QLabel#title {{
                color: {colors.TEXT};
                font-size: 30px;
                font-weight: 700;
            }}

            QLabel#subtitle {{
                color: {colors.TEXT};
                font-size: 16px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(18)

        title = QLabel("🩺 MedLens")
        title.setObjectName("title")

        subtitle = QLabel(
            "AI Medical Assistant\n\nHow can I help you today?"
        )
        subtitle.setObjectName("subtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        cards = [
            (
                "🎤",
                "Talk to MedLens",
                "Ask questions about your medicines."
            ),
            (
                "📷",
                "Scan Medicine",
                "Identify medicines using Computer Vision."
            ),
            (
                "💊",
                "My Medicines",
                "View and manage saved medicines."
            ),
        ]

        for icon, title, desc in cards:
            layout.addWidget(FeatureCard(icon, title, desc))

        layout.addStretch()