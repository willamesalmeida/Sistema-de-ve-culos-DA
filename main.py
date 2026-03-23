"""
main.py
Application entry point.
"""
import sys
from PySide6.QtWidgets import QApplication
from app.core.database import initialize_database
from app.ui.main_window import MainWindow


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Initializes all services and launches the application."""
    initialize_database()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()