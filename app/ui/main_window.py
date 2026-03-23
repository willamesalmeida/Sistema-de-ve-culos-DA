"""
main_window.py
Main application window.
"""

import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel,
    QHBoxLayout, QVBoxLayout, QPushButton
)
from PySide6.QtGui import QFont, QPixmap, QIcon
from PySide6.QtCore import Qt, QSize
import qtawesome as qta
from app.ui.register_screen import RegisterScreen


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Veículos")
        self.setMinimumSize(900, 700)
        self._build_ui()

    def _build_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self._build_header())

        body = QWidget()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        body_layout.addWidget(self._build_sidebar())

        self.content_area = QWidget()
        self.content_area.setStyleSheet("background-color: white;")
        body_layout.addWidget(self.content_area, stretch=1)

        content_layout = QVBoxLayout(self.content_area)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_label = QLabel()
        logo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "assets", "images", "logo.png"
        )
        logo_pixmap = QPixmap(logo_path)
        logo_label.setPixmap(logo_pixmap.scaledToWidth(
            250, Qt.TransformationMode.SmoothTransformation
        ))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(logo_label)

        main_layout.addWidget(body, stretch=1)

    def _build_header(self) -> QWidget:
        """Builds the top header bar."""
        header = QWidget()
        header.setFixedHeight(60)
        header.setStyleSheet("background-color: #1565C0;")

        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 0, 20, 0)

        icon_label = QLabel()
        icon_label.setPixmap(qta.icon("fa5s.truck", color="white").pixmap(QSize(28, 28)))
        layout.addWidget(icon_label)

        title = QLabel("  Sistema de Veículos")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        layout.addWidget(title)

        layout.addStretch()

        return header

    def _build_sidebar(self) -> QWidget:
        """Builds the left navigation sidebar."""
        sidebar = QWidget()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("background-color: #1976D2;")

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(1)

        layout.addStretch(6)

        # ← NOVO: botão Início
        btn_home = self._create_nav_button(
            "  Início",
            qta.icon("fa5s.home", color="white")
        )
        btn_home.clicked.connect(self._show_home)
        layout.addWidget(btn_home)

        layout.addSpacing(20)

        btn_search = self._create_nav_button(
            "  Consulta",
            qta.icon("fa5s.search", color="white")
        )
        btn_search.clicked.connect(lambda: print("Consulta clicado"))
        layout.addWidget(btn_search)

        layout.addSpacing(20)

        btn_register = self._create_nav_button(
            "  Cadastro",
            qta.icon("fa5s.user-plus", color="white")
        )
        btn_register.clicked.connect(self._show_register_screen)
        layout.addWidget(btn_register)

        layout.addStretch(10)

        return sidebar

    def _create_nav_button(self, text: str, icon: QIcon) -> QPushButton:
        """Creates a styled navigation button for the sidebar."""
        btn = QPushButton(icon, text)
        btn.setIconSize(QSize(20, 20))
        btn.setFixedHeight(45)
        btn.setFont(QFont("Segoe UI", 11))
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 6px;
                text-align: left;
                padding-left: 50px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)
        return btn

    def _clear_content_area(self) -> None:
        """Removes all widgets from the content area."""
        layout = self.content_area.layout()
        if layout:
            while layout.count():
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

    def _show_home(self) -> None:                          # ← NOVO
        """Loads the home screen with company logo into the content area."""
        self._clear_content_area()

        layout = self.content_area.layout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_label = QLabel()
        logo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "assets", "images", "logo.png"
        )
        logo_pixmap = QPixmap(logo_path)
        logo_label.setPixmap(logo_pixmap.scaledToWidth(
            250, Qt.TransformationMode.SmoothTransformation
        ))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)

    def _show_register_screen(self) -> None:
        """Loads the registration screen into the content area."""
        self._clear_content_area()
        screen = RegisterScreen(self.content_area)
        screen.navigate_home.connect(self._show_home)    # ← NOVO
        self.content_area.layout().addWidget(screen)