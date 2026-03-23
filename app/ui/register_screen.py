"""
register_screen.py
Driver and vehicle registration screen.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QLineEdit, QGridLayout,
    QPushButton, QFileDialog                        # ← ALTERADO
)
from PySide6.QtGui import QFont, QPixmap            # ← ALTERADO
from PySide6.QtCore import Qt, QSize, Signal
import qtawesome as qta
import os                                           # ← NOVO
from app.core.plate_validator import validate_plate
from app.core.drivers_repository import create_driver
from app.core.vehicles_repository import create_vehicle
from app.ui.components.message_dialog import MessageDialog


class RegisterScreen(QWidget):
    """Registration screen for drivers and vehicles."""

    navigate_home = Signal()

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self._field_name:    QLineEdit = None
        self._field_cpf:     QLineEdit = None
        self._field_phone:   QLineEdit = None
        self._field_dept:    QLineEdit = None
        self._field_plate:   QLineEdit = None
        self._field_model:   QLineEdit = None
        self._photo_path:    str       = None    # ← NOVO
        self._photo_preview: QLabel    = None    # ← NOVO
        self._photo_label:   QLabel    = None    # ← NOVO

        self._build_ui()

    def _build_ui(self) -> None:
        """Builds the registration screen layout."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(0)
        self.setStyleSheet("background-color: white;")

        card = self._build_card()
        card.setMaximumWidth(800)
        main_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignTop)
        main_layout.addStretch()

    def _build_card(self) -> QFrame:
        """Builds the main form card."""
        card = QFrame()
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

        required_label = QLabel("* Campos obrigatórios")
        required_label.setFont(QFont("Segoe UI", 8))
        required_label.setStyleSheet("color: #9E9E9E; border: none;")
        required_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(required_label)

        layout.addWidget(self._build_form_fields())
        layout.addWidget(self._build_form_actions())

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
            QPushButton:hover {
                background-color: #BBDEFB;
            }
            QPushButton:pressed {
                background-color: #90CAF9;
            }
        """)
        btn_back.clicked.connect(self.navigate_home.emit)
        layout.addWidget(btn_back)

        icon_label = QLabel()
        icon_label.setPixmap(
            qta.icon("fa5s.user-plus", color="white").pixmap(QSize(18, 18))
        )
        icon_label.setFixedSize(36, 36)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("""
            background-color: #1565C0;
            border-radius: 18px;
        """)
        layout.addWidget(icon_label)

        title = QLabel("Cadastrar Motorista e Veículo")
        title.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        title.setStyleSheet("color: #212121; border: none;")
        layout.addWidget(title)

        layout.addStretch()

        return header

    def _build_form_fields(self) -> QWidget:
        """Builds the form input fields in a grid layout."""
        container = QWidget()
        container.setStyleSheet("border: none;")
        grid = QGridLayout(container)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(12)

        self._field_name,  name_w  = self._build_field("Nome completo", "João Silva", required=True)
        self._field_cpf,   cpf_w   = self._build_field("CPF", "000.000.000-00")
        self._field_phone, phone_w = self._build_field("Telefone", "(82) 99999-9999")
        self._field_dept,  dept_w  = self._build_field("Setor", "Logística")
        self._field_plate, plate_w = self._build_field("Placa", "ABC-1234 ou ABC1D23", required=True)
        self._field_model, model_w = self._build_field("Modelo do veículo", "Ex: VW 17.190")

        grid.addWidget(name_w,  0, 0)
        grid.addWidget(cpf_w,   0, 1)
        grid.addWidget(phone_w, 1, 0)
        grid.addWidget(dept_w,  1, 1)
        grid.addWidget(plate_w, 2, 0)
        grid.addWidget(model_w, 2, 1)

        # ← NOVO: campo de foto ocupa as duas colunas
        outer = QWidget()
        outer.setStyleSheet("border: none;")
        outer_layout = QVBoxLayout(outer)
        outer_layout.setContentsMargins(0, 8, 0, 0)
        outer_layout.setSpacing(0)
        outer_layout.addWidget(self._build_photo_field())
        grid.addWidget(outer, 3, 0, 1, 2)

        return container

    def _build_field(self, label: str, placeholder: str, required: bool = False) -> tuple:
        """
        Builds a labeled input field.

        Args:
            label:       Field label text.
            placeholder: Placeholder text shown inside the input.
            required:    If True, adds an asterisk to the label.

        Returns:
            Tuple of (QLineEdit, container QWidget)
        """
        container = QWidget()
        container.setStyleSheet("border: none;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        label_text = f"{label} *" if required else label
        lbl = QLabel(label_text)
        lbl.setFont(QFont("Segoe UI", 9))
        lbl.setStyleSheet("color: #616161; border: none;")
        layout.addWidget(lbl)

        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        field.setFixedHeight(36)
        field.setFont(QFont("Segoe UI", 10))
        field.setStyleSheet("""
            QLineEdit {
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                padding-left: 10px;
                color: #212121;
                background-color: white;
            }
            QLineEdit:focus {
                border: 1px solid #1565C0;
            }
        """)
        layout.addWidget(field)

        return field, container

    def _build_photo_field(self) -> QWidget:              # ← NOVO
        """Builds the photo upload field."""
        container = QWidget()
        container.setStyleSheet("border: none;")
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        lbl = QLabel("Foto do motorista")
        lbl.setFont(QFont("Segoe UI", 9))
        lbl.setStyleSheet("color: #616161; border: none;")
        layout.addWidget(lbl)

        upload_area = QWidget()
        upload_area.setFixedHeight(80)
        upload_area.setCursor(Qt.CursorShape.PointingHandCursor)
        upload_area.setStyleSheet("""
            QWidget {
                border: 2px dashed #BDBDBD;
                border-radius: 8px;
                background-color: #FAFAFA;
            }
            QWidget:hover {
                border-color: #1565C0;
                background-color: #E3F2FD;
            }
        """)

        area_layout = QHBoxLayout(upload_area)
        area_layout.setContentsMargins(16, 0, 16, 0)
        area_layout.setSpacing(16)

        self._photo_preview = QLabel()
        self._photo_preview.setFixedSize(52, 52)
        self._photo_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._photo_preview.setStyleSheet("""
            border: none;
            border-radius: 26px;
            background-color: #E0E0E0;
        """)
        self._photo_preview.setPixmap(
            qta.icon("fa5s.user", color="#9E9E9E").pixmap(QSize(26, 26))
        )
        area_layout.addWidget(self._photo_preview)

        text_container = QWidget()
        text_container.setStyleSheet("border: none; background: transparent;")
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)

        self._photo_label = QLabel("Clique para selecionar")
        self._photo_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self._photo_label.setStyleSheet("color: #1565C0; border: none; background: transparent;")
        text_layout.addWidget(self._photo_label)

        hint = QLabel("JPG ou PNG • Máx. 5MB")
        hint.setFont(QFont("Segoe UI", 9))
        hint.setStyleSheet("color: #9E9E9E; border: none; background: transparent;")
        text_layout.addWidget(hint)

        area_layout.addWidget(text_container)
        area_layout.addStretch()

        upload_area.mousePressEvent = lambda _: self._select_photo()

        layout.addWidget(upload_area)

        return container

    def _select_photo(self) -> None:                      # ← NOVO
        """Opens file dialog to select a driver photo."""
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar foto do motorista",
            "",
            "Imagens (*.jpg *.jpeg *.png)"
        )

        if not path:
            return

        if os.path.getsize(path) > 5 * 1024 * 1024:
            MessageDialog.warning(self, "A foto deve ter no máximo 5MB.")
            return

        self._photo_path = path

        pixmap = QPixmap(path).scaled(
            52, 52,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self._photo_preview.setPixmap(pixmap)
        self._photo_preview.setStyleSheet("""
            border: none;
            border-radius: 26px;
        """)

        filename = os.path.basename(path)
        self._photo_label.setText(filename)
        self._photo_label.setStyleSheet("color: #212121; border: none; background: transparent;")

    def _build_form_actions(self) -> QWidget:
        """Builds the form action buttons (save and clear)."""
        container = QWidget()
        container.setStyleSheet("border: none;")
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 8, 0, 0)
        layout.setSpacing(8)

        layout.addStretch()

        btn_clear = QPushButton("Limpar")
        btn_clear.setFixedHeight(38)
        btn_clear.setFixedWidth(100)
        btn_clear.setFont(QFont("Segoe UI", 10))
        btn_clear.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_clear.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #616161;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #F5F5F5;
                border: 1px solid #BDBDBD;
            }
            QPushButton:pressed {
                background-color: #EEEEEE;
            }
        """)
        btn_clear.clicked.connect(self._on_clear)
        layout.addWidget(btn_clear)

        btn_save = QPushButton("Salvar")
        btn_save.setFixedHeight(38)
        btn_save.setFixedWidth(100)
        btn_save.setFont(QFont("Segoe UI", 10))
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.setStyleSheet("""
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
        btn_save.clicked.connect(self._on_save)
        layout.addWidget(btn_save)

        return container

    def _on_save(self) -> None:
        """Validates and saves the driver and vehicle to the database."""
        name  = self._field_name.text().strip()
        cpf   = self._field_cpf.text().strip()
        phone = self._field_phone.text().strip()
        dept  = self._field_dept.text().strip()
        plate = self._field_plate.text().strip()
        model = self._field_model.text().strip()

        if not name:
            MessageDialog.warning(self, "O nome do motorista é obrigatório.")
            self._field_name.setFocus()
            return

        if not plate:
            MessageDialog.warning(self, "A placa do veículo é obrigatória.")
            self._field_plate.setFocus()
            return

        result = validate_plate(plate)
        if not result.is_valid:
            MessageDialog.warning(self, result.message)
            self._field_plate.setFocus()
            return

        try:
            driver = create_driver(
                name=name,
                cpf=cpf or None,
                phone=phone or None,
                department=dept or None,
                photo_path=self._photo_path or None,    # ← NOVO
            )
            create_vehicle(
                plate=result.normalized,
                model=model or None,
                driver_id=driver.id,
            )
            MessageDialog.success(
                self,
                f"Motorista '{name}' e veículo '{result.normalized}' cadastrados com sucesso!"
            )
            self._on_clear()

        except Exception as e:
            error = str(e)
            if "UNIQUE constraint failed: vehicles.plate" in error:
                MessageDialog.error(self, "Essa placa já está cadastrada no sistema.")
            else:
                MessageDialog.error(self, "Ocorreu um erro ao salvar. Tente novamente.")

    def _on_clear(self) -> None:
        """Clears all form fields."""
        self._field_name.clear()
        self._field_cpf.clear()
        self._field_phone.clear()
        self._field_dept.clear()
        self._field_plate.clear()
        self._field_model.clear()
        self._field_name.setFocus()

        # ← NOVO: reseta o campo de foto
        self._photo_path = None
        self._photo_preview.setPixmap(
            qta.icon("fa5s.user", color="#9E9E9E").pixmap(QSize(26, 26))
        )
        self._photo_preview.setStyleSheet("""
            border: none;
            border-radius: 26px;
            background-color: #E0E0E0;
        """)
        self._photo_label.setText("Clique para selecionar")
        self._photo_label.setStyleSheet("color: #1565C0; border: none; background: transparent;")