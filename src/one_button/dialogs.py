from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QFileDialog, QDialogButtonBox
from .config import ACTION_NAMES_RU, ACTION_NAMES_EN, tr

class ActionDialog(QDialog):
    def __init__(self, parent=None, language="ru", existing=None):
        super().__init__(parent)
        self.language = language
        self.existing = existing or {}

        self.setWindowTitle(tr(language, "action"))
        self.setMinimumWidth(560)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        layout.addWidget(QLabel(tr(language, "action_type")))

        self.type_box = QComboBox()
        names = ACTION_NAMES_RU if language == "ru" else ACTION_NAMES_EN
        for key, label in names.items():
            self.type_box.addItem(label, key)

        self.value = QLineEdit()
        self.value.setPlaceholderText(tr(language, "value_placeholder"))

        self.browse = QPushButton(tr(language, "browse"))

        layout.addWidget(self.type_box)
        layout.addWidget(self.value)
        layout.addWidget(self.browse)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText(tr(language, "save"))
        buttons.button(QDialogButtonBox.Cancel).setText(tr(language, "cancel"))
        layout.addWidget(buttons)

        self.type_box.currentIndexChanged.connect(self.refresh)
        self.browse.clicked.connect(self.browse_value)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        if existing:
            idx = self.type_box.findData(existing.get("type"))
            if idx >= 0:
                self.type_box.setCurrentIndex(idx)
            self.value.setText(existing.get("value", ""))

        self.refresh()

    def refresh(self):
        typ = self.type_box.currentData()
        self.browse.setVisible(typ in ("launch", "file", "folder"))

        placeholders = {
            "launch": "Путь к .exe" if self.language == "ru" else "Path to .exe",
            "website": "https://example.com",
            "close": "chrome.exe",
            "wait": "2",
            "command": "ipconfig /flushdns",
        }
        self.value.setPlaceholderText(
            placeholders.get(typ, tr(self.language, "value_placeholder"))
        )

    def browse_value(self):
        typ = self.type_box.currentData()
        if typ == "launch":
            path, _ = QFileDialog.getOpenFileName(
                self, "Выберите приложение", "", "Программы (*.exe);;Все файлы (*.*)"
            )
        elif typ == "file":
            path, _ = QFileDialog.getOpenFileName(
                self, "Выберите файл", "", "Все файлы (*.*)"
            )
        else:
            path = QFileDialog.getExistingDirectory(self, "Выберите папку")

        if path:
            self.value.setText(path)

    def result_action(self):
        return {
            "type": self.type_box.currentData(),
            "value": self.value.text().strip(),
        }

