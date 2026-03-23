"""
search_screen.py
Vehicle search screen by plate number.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame,
    QGridLayout
)
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt, QSize, Signal
import qtawesome as qta
import os
from app.core.plate_validator import validate_plate
from app.core.vehicles_repository import get_vehicle_by_plate
from app.ui.components.message_dialog import MessageDialog


class SearchScreen(QWidget):
    """Vehicle search screen by plate number."""

    navigate_home = Signal()

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._result_area   = None
        self._result_layout = None
        self._build_ui()

    def _build_ui(self) -> None:
        """Builds the search screen layout."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        self.setStyleSheet("background-color: white;")

        main_layout.addWidget(self._build_search_card())

        # ← NOVO: área do card de resultado
        self._result_area = QWidget()
        self._result_area.setStyleSheet("border: none;")
        self._result_area.setMaximumWidth(800)
        self._result_layout = QVBoxLayout(self._result_area)
        self._result_layout.setContentsMargins(0, 0, 0, 0)
        self._result_layout.setSpacing(0)
        main_layout.addWidget(self._result_area)

        main_layout.addStretch()

    def _build_search_card(self) -> QFrame:
        """Builds the search input card."""
        card = QFrame()
        card.setMaximumWidth(800)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #E0E0E0;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        layout.addWidget(self._build_card_header())

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("border: none; border-top: 1px solid #E0E0E0;")
        layout.addWidget(separator)

        layout.addWidget(self._build_search_field())

        return card

    def _build_card_header(self) -> QWidget:
        """Builds the card header with icon and title."""
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        btn_back = QPushButton()
        btn_back.setIcon(qta.icon("fa5s.arrow-left", color="#1565C0"))
        btn_back.setIconSize(QSize(16, 16))
        btn_back.setFixedSize(32, 32)
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.setToolTip("Voltar para o início")
        btn_back.setStyleSheet("""
            QPushButton {
                background-color: #E3F2FD;
                border: none;
                border-radius: 16px;
            }
            QPushButton:hover { background-color: #BBDEFB; }
            QPushButton:pressed { background-color: #90CAF9; }
        """)
        btn_back.clicked.connect(self.navigate_home.emit)
        layout.addWidget(btn_back)

        icon_label = QLabel()
        icon_label.setPixmap(
            qta.icon("fa5s.search", color="white").pixmap(QSize(18, 18))
        )
        icon_label.setFixedSize(36, 36)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("""
            background-color: #1565C0;
            border-radius: 18px;
        """)
        layout.addWidget(icon_label)

        title = QLabel("Consultar Veículo por Placa")
        title.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        title.setStyleSheet("color: #212121; border: none;")
        layout.addWidget(title)

        layout.addStretch()
        return header

    def _build_search_field(self) -> QWidget:
        """Builds the plate input field with search button."""
        container = QWidget()
        container.setStyleSheet("border: none;")
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        field_col = QWidget()
        field_col.setStyleSheet("border: none;")
        field_layout = QVBoxLayout(field_col)
        field_layout.setContentsMargins(0, 0, 0, 0)
        field_layout.setSpacing(6)

        lbl = QLabel("Número da placa")
        lbl.setFont(QFont("Segoe UI", 12))
        lbl.setStyleSheet("color: #616161; border: none;")
        field_layout.addWidget(lbl)

        self._field_plate = QLineEdit()
        self._field_plate.setPlaceholderText("Ex: ABC-1234 ou ABC1D23")
        self._field_plate.setFixedHeight(42)
        self._field_plate.setFont(QFont("Segoe UI", 12))
        self._field_plate.setStyleSheet("""
            QLineEdit {
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                padding-left: 14px;
                color: #212121;
                background-color: white;
            }
            QLineEdit:focus { border: 1px solid #1565C0; }
        """)
        self._field_plate.returnPressed.connect(self._on_search)
        field_layout.addWidget(self._field_plate)

        layout.addWidget(field_col, stretch=1)

        btn_wrapper = QWidget()
        btn_wrapper.setStyleSheet("border: none;")
        btn_wrapper_layout = QVBoxLayout(btn_wrapper)
        btn_wrapper_layout.setContentsMargins(0, 0, 0, 0)
        btn_wrapper_layout.setSpacing(6)
        btn_wrapper_layout.addStretch()

        btn_search = QPushButton(
            qta.icon("fa5s.search", color="white"), "  Buscar"
        )
        btn_search.setFixedHeight(42)
        btn_search.setFixedWidth(120)
        btn_search.setFont(QFont("Segoe UI", 10))
        btn_search.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_search.setStyleSheet("""
            QPushButton {
                background-color: #1565C0;
                color: white;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover { background-color: #1976D2; }
            QPushButton:pressed { background-color: #0D47A1; }
        """)
        btn_search.clicked.connect(self._on_search)
        btn_wrapper_layout.addWidget(btn_search)

        layout.addWidget(btn_wrapper)
        return container

    def _on_search(self) -> None:
        """Handles the search action."""
        raw = self._field_plate.text().strip()

        if not raw:
            MessageDialog.warning(self, "Digite uma placa para consultar.")
            self._field_plate.setFocus()
            return

        result = validate_plate(raw)
        if not result.is_valid:
            MessageDialog.warning(self, result.message)
            self._field_plate.setFocus()
            return

        data = get_vehicle_by_plate(result.normalized)

        if not data:
            MessageDialog.warning(
                self,
                f"Nenhum veículo encontrado com a placa {result.normalized}."
            )
            return

        self._show_result(data)

    def _show_result(self, data) -> None:
        """Displays the CNH-style result card."""
        while self._result_layout.count():
            item = self._result_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self._result_layout.addWidget(self._build_result_card(data))

    def _build_result_card(self, data) -> QFrame:
        """Builds the CNH-style card with vehicle and driver data."""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 2px solid #1565C0;
            }
        """)

        layout = QHBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        stripe = QWidget()
        stripe.setFixedWidth(12)
        stripe.setStyleSheet(
            "background-color: #1565C0; border-radius: 10px 0 0 10px; border: none;"
        )
        layout.addWidget(stripe)

        layout.addWidget(self._build_photo_section(data.driver))
        layout.addWidget(self._build_divider())
        layout.addWidget(self._build_driver_section(data.driver), stretch=1)
        layout.addWidget(self._build_divider())
        layout.addWidget(self._build_vehicle_section(data.vehicle))

        return card

    def _build_photo_section(self, driver) -> QWidget:
        """Builds the photo section of the result card."""
        container = QWidget()
        container.setStyleSheet("border: none; background-color: white;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 16, 20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        photo_label = QLabel()
        photo_label.setFixedSize(90, 110)
        photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        photo_label.setStyleSheet("""
            border: 2px solid #E0E0E0;
            border-radius: 8px;
            background-color: #F5F5F5;
        """)

        loaded = False
        if driver and driver.photo_path and os.path.exists(driver.photo_path):
            pixmap = QPixmap(driver.photo_path).scaled(
                90, 110,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            photo_label.setPixmap(pixmap)
            loaded = True

        if not loaded:
            photo_label.setPixmap(
                qta.icon("fa5s.user", color="#BDBDBD").pixmap(QSize(40, 40))
            )

        layout.addWidget(photo_label)
        return container

    def _build_divider(self) -> QWidget:
        """Builds a vertical divider."""
        divider = QWidget()
        divider.setFixedWidth(1)
        divider.setStyleSheet("background-color: #E0E0E0; border: none;")
        return divider

    def _build_driver_section(self, driver) -> QWidget:
        """Builds the driver data section."""
        container = QWidget()
        container.setStyleSheet("border: none; background-color: white;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(8)

        badge = QLabel("MOTORISTA")
        badge.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        badge.setStyleSheet("""
            background-color: #1565C0;
            color: white;
            border-radius: 10px;
            padding: 2px 10px;
            border: none;
        """)
        badge.setFixedHeight(22)
        badge.setMaximumWidth(100)
        layout.addWidget(badge)

        if not driver:
            msg = QLabel("Nenhum motorista vinculado a este veículo.")
            msg.setFont(QFont("Segoe UI", 10))
            msg.setStyleSheet("color: #9E9E9E; border: none;")
            layout.addWidget(msg)
            layout.addStretch()
            return container

        name = QLabel(driver.name)
        name.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        name.setStyleSheet("color: #212121; border: none;")
        layout.addWidget(name)

        grid_widget = QWidget()
        grid_widget.setStyleSheet("border: none;")
        grid = QGridLayout(grid_widget)
        grid.setContentsMargins(0, 4, 0, 0)
        grid.setSpacing(8)
        grid.setHorizontalSpacing(24)

        fields = [
            ("CPF",           driver.cpf       or "—"),
            ("Telefone",      driver.phone      or "—"),
            ("Setor",         driver.department or "—"),
            ("Cadastrado em", driver.created_at[:10] if driver.created_at else "—"),
        ]

        for i, (label_text, value_text) in enumerate(fields):
            row, col = divmod(i, 2)

            cell = QWidget()
            cell.setStyleSheet("border: none;")
            cell_layout = QVBoxLayout(cell)
            cell_layout.setContentsMargins(0, 0, 0, 0)
            cell_layout.setSpacing(1)

            lbl = QLabel(label_text)
            lbl.setFont(QFont("Segoe UI", 9))
            lbl.setStyleSheet("color: #9E9E9E; border: none;")

            val = QLabel(value_text)
            val.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
            val.setStyleSheet("color: #212121; border: none;")

            cell_layout.addWidget(lbl)
            cell_layout.addWidget(val)
            grid.addWidget(cell, row, col)

        layout.addWidget(grid_widget)
        layout.addStretch()
        return container

    def _build_vehicle_section(self, vehicle) -> QWidget:
        """Builds the vehicle data section."""
        container = QWidget()
        container.setFixedWidth(200)
        container.setStyleSheet("""
            background-color: #F5F7FA;
            border-radius: 0 10px 10px 0;
            border: none;
        """)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(10)

        badge = QLabel("VEÍCULO")
        badge.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        badge.setStyleSheet("""
            background-color: #2E7D32;
            color: white;
            border-radius: 10px;
            padding: 2px 10px;
            border: none;
        """)
        badge.setFixedHeight(22)
        badge.setMaximumWidth(80)
        layout.addWidget(badge)

        plate_box = QFrame()
        plate_box.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #212121;
                border-radius: 6px;
            }
        """)
        plate_box.setFixedHeight(40)
        plate_layout = QHBoxLayout(plate_box)
        plate_layout.setContentsMargins(8, 0, 8, 0)

        plate_label = QLabel(vehicle.plate)
        plate_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        plate_label.setStyleSheet(
            "color: #212121; border: none; letter-spacing: 2px;"
        )
        plate_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        plate_layout.addWidget(plate_label)
        layout.addWidget(plate_box)

        model_lbl = QLabel("Modelo")
        model_lbl.setFont(QFont("Segoe UI", 9))
        model_lbl.setStyleSheet("color: #9E9E9E; border: none;")

        model_val = QLabel(vehicle.model or "—")
        model_val.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        model_val.setStyleSheet("color: #212121; border: none;")
        model_val.setWordWrap(True)

        layout.addWidget(model_lbl)
        layout.addWidget(model_val)
        layout.addStretch()

        return container