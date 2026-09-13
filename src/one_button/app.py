import sys
from PySide6.QtWidgets import QApplication
from .config import APP_NAME
from .window import MainWindow
from .style import APP_STYLE

def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setStyleSheet(APP_STYLE)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
