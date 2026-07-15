from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)


class FeatureCard(QFrame):
    """
    Reusable dashboard card.

    Parameters
    ----------
    icon : str
    title : str
    description : str
    """

    clicked = Signal()

    def __init__(self, icon: str, title: str, description: str):
        super().__init__()

        self.setCursor(Qt.PointingHandCursor)
        self.setObjectName("featureCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(6)

        icon_label = QLabel(icon)
        icon_label.setObjectName("icon")

        title_label = QLabel(title)
        title_label.setObjectName("title")

        desc_label = QLabel(description)
        desc_label.setObjectName("description")
        desc_label.setWordWrap(True)

        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(desc_label)

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)