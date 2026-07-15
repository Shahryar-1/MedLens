from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QStackedWidget,
)

from app.ui.widgets.bottom_navigation import BottomNavigation
from app.ui.pages.dashboard_page import DashboardPage
from app.ui.pages.scan_page import ScanPage
from app.ui.pages.medicines_page import MedicinesPage
from app.ui.pages.reminders_page import RemindersPage
from app.ui.pages.help_page import HelpPage
from app.ui.pages.settings_page import SettingsPage


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("MedLens")
        self.resize(1200, 700)

        self.setup_ui()

    def setup_ui(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        self.pages = QStackedWidget()

        self.bottom_nav = BottomNavigation()
        self.dashboard_page = DashboardPage()
        self.scan_page = ScanPage()
        self.medicines_page = MedicinesPage()
        self.reminders_page = RemindersPage()
        self.help_page = HelpPage()
        self.settings_page = SettingsPage()

        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.scan_page)
        self.pages.addWidget(self.medicines_page)
        self.pages.addWidget(self.reminders_page)
        self.pages.addWidget(self.help_page)
        self.pages.addWidget(self.settings_page)

        layout.addWidget(self.pages)
        layout.addWidget(self.bottom_nav)
        layout.addWidget(self.pages)
        self.bottom_nav.page_changed.connect(self.change_page)
    def change_page(self, index: int):
        """Switch pages."""

        self.pages.setCurrentIndex(index)