"""
search_screen.py
Vehicle search screen by plate number.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame,
    QGridLayout, QMessageBox
)
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtCore import Qt, QSize, Signal
import qtawesome as qta
import os
from pathlib import Path

from app.core.plate_validator import validate_plate
from app.core.vehicles_repository import get_vehicle_by_plate, get_all_vehicles_with_drivers, delete_vehicle
from app.ui.components.message_dialog import MessageDialog


class SearchScreen(QWidget):
    """Vehicle search screen by plate number."""
    navigate_home = Signal()

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._result_area = None
        self._result_layout = None
        self._field_plate = None
        self._current_vehicle_id = None   # ← NOVO: guarda o ID para excluir
        self._build_ui()

    def _build_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        self.setStyleSheet("background-color: white;")

        main_layout.addWidget(self._build_search_card())

        self._result_area = QWidget()
        self._result_area.setStyleSheet("border: none;")
        self._result_area.setMaximumWidth(800)
        self._result_layout = QVBoxLayout(self._result_area)
        self._result_layout.setContentsMargins(0, 0, 0, 0)
        self._result_layout.setSpacing(0)
        main_layout.addWidget(self._result_area)

        main_layout.addStretch()

    def _build_search_card(self) -> QFrame:
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
        icon_label.setPixmap(qta.icon("fa5s.search", color="white").pixmap(QSize(18, 18)))
        icon_label.setFixedSize(36, 36)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("background-color: #1565C0; border-radius: 18px;")
        layout.addWidget(icon_label)

        title = QLabel("Consultar Veículo por Placa ou Nome")
        title.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        title.setStyleSheet("color: #212121; border: none;")
        layout.addWidget(title)
        layout.addStretch()
        return header

    # =============================================
    # ALTERAÇÃO FEITA AQUI
    # =============================================
    def _build_search_field(self) -> QWidget:
        """Campo de busca + botões Buscar e Limpar."""
        container = QWidget()
        container.setStyleSheet("border: none;")
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        field_col = QWidget()
        field_col.setStyleSheet("border: none;")
        field_layout = QVBoxLayout(field_col)
        field_layout.setContentsMargins(0, 0, 0, 0)
        field_layout.setSpacing(4)

        lbl = QLabel("Placa ou Nome do Motorista")
        lbl.setFont(QFont("Segoe UI", 12))
        lbl.setStyleSheet("color: #616161; border: none;")
        field_layout.addWidget(lbl)

        self._field_plate = QLineEdit()
        self._field_plate.setPlaceholderText("Ex: ABC1234, João Silva ou 'todos'")
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

        # Botão Buscar
        btn_search = QPushButton(qta.icon("fa5s.search", color="white"), " Buscar")
        btn_search.setFixedSize(120, 42)
        btn_search.setFont(QFont("Segoe UI", 10))
        btn_search.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_search.setStyleSheet("""
            QPushButton { background-color: #1565C0; color: white; border: none; border-radius: 6px; }
            QPushButton:hover { background-color: #1976D2; }
            QPushButton:pressed { background-color: #0D47A1; }
        """)
        btn_search.clicked.connect(self._on_search)

        # Botão Limpar
        btn_clear = QPushButton("Limpar")
        btn_clear.setFixedSize(100, 42)
        btn_clear.setFont(QFont("Segoe UI", 10))
        btn_clear.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_clear.setStyleSheet("""
            QPushButton { background-color: white; color: #616161; border: 1px solid #E0E0E0; border-radius: 6px; }
            QPushButton:hover { background-color: #F5F5F5; border: 1px solid #BDBDBD; }
            QPushButton:pressed { background-color: #EEEEEE; }
        """)
        btn_clear.clicked.connect(self._on_clear_search)

        layout.addWidget(btn_search, alignment=Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(btn_clear, alignment=Qt.AlignmentFlag.AlignBottom)

        return container
    # =============================================
    # FIM DA ALTERAÇÃO
    # =============================================

    def _on_search(self) -> None:
        """Busca por placa, nome ou 'todos'."""
        text = self._field_plate.text().strip().lower()

        if text == "" or text == "todos":
            data_list = get_all_vehicles_with_drivers()
            if not data_list:
                MessageDialog.warning(self, "Nenhum cadastro encontrado no banco.")
                return
            # Mostra o primeiro (ou podemos criar uma lista no futuro)
            self._show_result(data_list[0])   # por enquanto mostra o primeiro
            return

        # Tenta como placa
        result = validate_plate(text.upper())
        if result.is_valid:
            data = get_vehicle_by_plate(result.normalized)
            if data:
                self._show_result(data)
                return

        # Se não for placa válida, busca por nome do motorista
        data = get_vehicle_by_plate(text)  # por enquanto usamos a mesma função (futuramente vamos melhorar)
        if data:
            self._show_result(data)
        else:
            MessageDialog.warning(self, f"Nenhum veículo encontrado com '{text}'.")

    def _on_clear_search(self) -> None:
        """Limpa o campo e remove o card de resultado."""
        self._field_plate.clear()
        self._field_plate.setFocus()

        while self._result_layout.count():
            item = self._result_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _show_result(self, data) -> None:
        while self._result_layout.count():
            item = self._result_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        card = self._build_result_card(data)
        self._result_layout.addWidget(card)

    # =============================================
    # NOVO: Botão Excluir dentro do card
    # =============================================
    def _build_result_card(self, data) -> QFrame:
        card = QFrame()
        card.setStyleSheet("""
            QFrame { background-color: white; border-radius: 12px; border: 2px solid #1565C0; }
        """)
        layout = QHBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        stripe = QWidget()
        stripe.setFixedWidth(12)
        stripe.setStyleSheet("background-color: #1565C0; border-radius: 10px 0 0 10px;")
        layout.addWidget(stripe)

        layout.addWidget(self._build_photo_section(data.driver))
        layout.addWidget(self._build_divider())
        layout.addWidget(self._build_driver_section(data.driver), stretch=1)
        layout.addWidget(self._build_divider())
        layout.addWidget(self._build_vehicle_section(data.vehicle))

        # Botão Excluir no final do card
        delete_btn = QPushButton(qta.icon("fa5s.trash", color="white"), " Excluir")
        delete_btn.setFixedHeight(40)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #C62828;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0 20px;
            }
            QPushButton:hover { background-color: #E53935; }
        """)
        delete_btn.clicked.connect(lambda: self._on_delete(data.vehicle.id))

        # Adiciona o botão no layout inferior
        bottom_layout = QVBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(delete_btn, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addLayout(bottom_layout)

        return card

    def _on_delete(self, vehicle_id: int) -> None:
        """Exclui o cadastro após confirmação."""
        reply = QMessageBox.question(
            self, "Confirmar exclusão",
            "Tem certeza que deseja excluir este cadastro?\nEsta ação não pode ser desfeita.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            if delete_vehicle(vehicle_id):
                MessageDialog.success(self, "Cadastro excluído com sucesso!")
                self._on_clear_search()   # limpa o card
            else:
                MessageDialog.error(self, "Erro ao excluir o cadastro.")

    # (os métodos _build_photo_section, _build_divider, _build_driver_section e _build_vehicle_section permanecem iguais)
    # ... (resto do arquivo mantido igual ao anterior)