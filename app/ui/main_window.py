from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QStackedWidget,
)

from app.ui.widgets.sidebar import Sidebar

from app.ui.pages.dashboard_page import DashboardPage
from app.ui.pages.scan_page import ScanPage
from app.ui.pages.medicines_page import MedicinesPage
from app.ui.pages.reminders_page import RemindersPage
from app.ui.pages.help_page import HelpPage
from app.ui.pages.settings_page import SettingsPage


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("MedLens")
        self.resize(1200, 700)

        self.setup_ui()

    def setup_ui(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        # ---------------- Sidebar ----------------

        self.sidebar = Sidebar()

        # ---------------- Pages ----------------

        self.pages = QStackedWidget()

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

        # ---------------- Layout ----------------

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.pages)

        # ---------------- Signals ----------------

        self.sidebar.page_changed.connect(self.change_page)

    def change_page(self, page_name):

        pages = {
            "dashboard": 0,
            "scan": 1,
            "medicines": 2,
            "reminders": 3,
            "help": 4,
            "settings": 5,
        }

        if page_name in pages:
            self.pages.setCurrentIndex(pages[page_name])