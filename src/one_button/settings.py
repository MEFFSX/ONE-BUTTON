from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QFrame, QComboBox, QCheckBox, QHBoxLayout, QPushButton, QLabel, QMessageBox
from .config import DEFAULT_DATA, tr, set_autostart, save_data

class SettingsPage(QWidget):
    changed = Signal()

    def __init__(self, data):
        super().__init__()
        self.data = data
        self.lang = data["settings"].get("language", "ru")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 34, 40, 34)
        layout.setSpacing(18)

        self.title = QLabel(tr(self.lang, "settings"))
        self.title.setObjectName("PageTitle")
        layout.addWidget(self.title)

        card = QFrame()
        card.setObjectName("Card")

        form = QFormLayout(card)
        form.setContentsMargins(26, 26, 26, 26)
        form.setSpacing(14)

        self.lang_box = QComboBox()
        self.lang_box.addItem("Русский", "ru")
        self.lang_box.addItem("English", "en")
        self.lang_box.setCurrentIndex(0 if self.lang == "ru" else 1)
        self.lang_label = QLabel(tr(self.lang, "language"))
        form.addRow(self.lang_label, self.lang_box)

        s = data["settings"]

        self.autostart = QCheckBox(tr(self.lang, "autostart"))
        self.autostart.setChecked(s.get("autostart", False))
        form.addRow(self.autostart)

        self.notifications = QCheckBox(tr(self.lang, "notifications"))
        self.notifications.setChecked(s.get("notifications", True))
        form.addRow(self.notifications)

        self.confirm_power = QCheckBox(tr(self.lang, "confirm_power_opt"))
        self.confirm_power.setChecked(s.get("confirm_power", True))
        form.addRow(self.confirm_power)

        self.minimize = QCheckBox(tr(self.lang, "minimize"))
        self.minimize.setChecked(s.get("minimize_after_run", False))
        form.addRow(self.minimize)

        layout.addWidget(card)

        btns = QHBoxLayout()
        btns.setSpacing(12)

        self.save_btn = QPushButton(tr(self.lang, "save_changes"))
        self.save_btn.setObjectName("PrimaryButton")
        self.save_btn.setMinimumHeight(46)
        self.save_btn.clicked.connect(self.apply)

        self.reset_btn = QPushButton(tr(self.lang, "reset"))
        self.reset_btn.setMinimumHeight(46)
        self.reset_btn.clicked.connect(self.reset)

        btns.addWidget(self.save_btn, 2)
        btns.addWidget(self.reset_btn, 1)

        layout.addLayout(btns)
        layout.addStretch()

        self.lang_box.currentIndexChanged.connect(self._relang)

    def _relang(self):
        self.lang = self.lang_box.currentData()
        self.title.setText(tr(self.lang, "settings"))
        self.lang_label.setText(tr(self.lang, "language"))
        self.autostart.setText(tr(self.lang, "autostart"))
        self.notifications.setText(tr(self.lang, "notifications"))
        self.confirm_power.setText(tr(self.lang, "confirm_power_opt"))
        self.minimize.setText(tr(self.lang, "minimize"))
        self.save_btn.setText(tr(self.lang, "save_changes"))
        self.reset_btn.setText(tr(self.lang, "reset"))

    def apply(self):
        s = self.data["settings"]
        s["language"] = self.lang_box.currentData()
        s["autostart"] = self.autostart.isChecked()
        s["notifications"] = self.notifications.isChecked()
        s["confirm_power"] = self.confirm_power.isChecked()
        s["minimize_after_run"] = self.minimize.isChecked()

        set_autostart(s["autostart"])
        save_data(self.data)

        self.changed.emit()

        QMessageBox.information(self, APP_NAME, tr(s["language"], "saved"))

    def reset(self):
        self.data["settings"] = DEFAULT_DATA["settings"].copy()
        self.lang = "ru"

        self.lang_box.setCurrentIndex(0)
        self.autostart.setChecked(False)
        self.notifications.setChecked(True)
        self.confirm_power.setChecked(True)
        self.minimize.setChecked(False)

        self._relang()
        set_autostart(False)
        save_data(self.data)
        self.changed.emit()

