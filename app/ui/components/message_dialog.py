"""
message_dialog.py
Standardized dialog component for success, warning and error messages.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QWidget
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QSize
import qtawesome as qta


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_DIALOG_CONFIGS = {
    "success": {
        "title":      "Sucesso",
        "icon":       "fa5s.check",
        "icon_color": "#2E7D32",
        "bg_color":   "#E8F5E9",
    },
    "warning": {
        "title":      "Atenção",
        "icon":       "fa5s.exclamation",
        "icon_color": "#F57F17",
        "bg_color":   "#FFF8E1",
    },
    "error": {
        "title":      "Erro",
        "icon":       "fa5s.times",
        "icon_color": "#C62828",
        "bg_color":   "#FFEBEE",
    },
}


# ---------------------------------------------------------------------------
# Dialog
# ---------------------------------------------------------------------------

class MessageDialog(QDialog):
    """
    Standardized styled dialog for user feedback messages.

    Usage:
        MessageDialog.success(parent, "Motorista cadastrado com sucesso!")
        MessageDialog.warning(parent, "O nome é obrigatório.")
        MessageDialog.error(parent, "Erro ao salvar os dados.")
    """

    def __init__(self, parent: QWidget, kind: str, message: str):
        super().__init__(parent)

        config = _DIALOG_CONFIGS[kind]

        self.setWindowTitle(config["title"])
        self.setFixedSize(360, 220)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._build_ui(config, message)

    def _build_ui(self, config: dict, message: str) -> None:
        """Builds the dialog layout."""
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        # Card
        card = QWidget()
        card.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 28, 24, 24)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Ícone
        icon_container = QWidget()
        icon_container.setFixedSize(56, 56)
        icon_container.setStyleSheet(f"""
            QWidget {{
                background-color: {config['bg_color']};
                border-radius: 28px;
                border: none;
            }}
        """)
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_label = QLabel()
        icon_label.setPixmap(
            qta.icon(config["icon"], color=config["icon_color"]).pixmap(QSize(24, 24))
        )
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("background: transparent; border: none;")
        icon_layout.addWidget(icon_label)

        icon_wrapper = QHBoxLayout()
        icon_wrapper.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_wrapper.addWidget(icon_container)
        layout.addLayout(icon_wrapper)

        # Título
        title = QLabel(config["title"])
        title.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        title.setStyleSheet("color: #212121; border: none;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Mensagem
        msg = QLabel(message)
        msg.setFont(QFont("Segoe UI", 10))
        msg.setStyleSheet("color: #757575; border: none;")
        msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg.setWordWrap(True)
        layout.addWidget(msg)

        # Botão OK
        btn_ok = QPushButton("OK")
        btn_ok.setFixedHeight(38)
        btn_ok.setFixedWidth(120)
        btn_ok.setFont(QFont("Segoe UI", 10))
        btn_ok.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_ok.setStyleSheet("""
            QPushButton {
                background-color: #1565C0;
                color: white;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        btn_ok.clicked.connect(self.accept)

        btn_wrapper = QHBoxLayout()
        btn_wrapper.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn_wrapper.addWidget(btn_ok)
        layout.addLayout(btn_wrapper)

        outer_layout.addWidget(card)

    # -----------------------------------------------------------------------
    # Static convenience methods
    # -----------------------------------------------------------------------

    @staticmethod
    def success(parent: QWidget, message: str) -> None:
        """Shows a success dialog."""
        MessageDialog(parent, "success", message).exec()

    @staticmethod
    def warning(parent: QWidget, message: str) -> None:
        """Shows a warning dialog."""
        MessageDialog(parent, "warning", message).exec()

    @staticmethod
    def error(parent: QWidget, message: str) -> None:
        """Shows an error dialog."""
        MessageDialog(parent, "error", message).exec()