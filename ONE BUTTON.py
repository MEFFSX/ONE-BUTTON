import sys
import os
import json
import subprocess
import time
from pathlib import Path

from PySide6.QtCore import Qt, QThread, Signal, QUrl
from PySide6.QtGui import QColor, QDesktopServices, QIcon
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QListWidget, QListWidgetItem, QStackedWidget,
    QLineEdit, QFileDialog, QMessageBox, QComboBox, QCheckBox, QDialog,
    QDialogButtonBox, QFrame, QScrollArea, QFormLayout, QGraphicsDropShadowEffect,
)

APP_NAME = "ONE BUTTON"

APP_DIR = Path(os.getenv("APPDATA", str(Path.home()))) / "OneButton"
DATA_FILE = APP_DIR / "data.json"

DEV_NAME = "MEFF¹"
DEV_TELEGRAM = "https://t.me/meffsnos"
DEV_DONATE = "https://t.me/meffsnos"


def resource_path(relative: str) -> Path:
    base = getattr(sys, "_MEIPASS", None)
    if base:
        return Path(base) / relative
    return Path(__file__).resolve().parent / relative


ICON_PATH = resource_path("ico.ico")


def load_icon() -> QIcon:
    if ICON_PATH.exists():
        return QIcon(str(ICON_PATH))
    return QIcon()


DEFAULT_DATA = {
    "settings": {
        "language": "ru",
        "accent": "#8B5CF6",
        "autostart": False,
        "notifications": True,
        "confirm_power": True,
        "minimize_after_run": False,
    },
    "profiles": [
        {"name": "Учёба", "accent": "#8B5CF6", "actions": []},
        {"name": "Работа", "accent": "#A855F7", "actions": []},
        {"name": "Игры", "accent": "#C084FC", "actions": []},
    ],
}

TEXTS = {
    "ru": {
        "profiles": "Профили",
        "settings": "Настройки",
        "new_profile": "+ НОВЫЙ ПРОФИЛЬ",
        "run": "ЗАПУСТИТЬ",
        "edit": "НАСТРОИТЬ",
        "delete": "УДАЛИТЬ",
        "delete_confirm_title": "Удалить профиль?",
        "delete_confirm_text": "Профиль «{}» будет удалён без возможности восстановления.",
        "subtitle": "PERSONAL AUTOMATION",
        "desc": "Одна кнопка — любая последовательность действий Windows.",
        "actions_count": "действий",
        "no_actions": "В этом профиле пока нет действий.",
        "confirm_title": "Подтверждение",
        "confirm_power": "содержит выключение или перезагрузку ПК.\n\nПродолжить?",
        "done": "Готово",
        "error": "Ошибка",
        "language": "Язык",
        "autostart": "Запускать ONE BUTTON вместе с Windows",
        "notifications": "Показывать уведомления после запуска",
        "confirm_power_opt": "Подтверждать выключение и перезагрузку",
        "minimize": "Сворачивать окно после запуска профиля",
        "save_changes": "СОХРАНИТЬ ИЗМЕНЕНИЯ",
        "reset": "Сбросить настройки",
        "saved": "Настройки сохранены",
        "profile_setup": "Настройка профиля",
        "profile_name": "Название",
        "add_action": "+ Добавить действие",
        "change": "Изменить",
        "remove": "Удалить",
        "drag_hint": "Перетаскивай действия мышкой, чтобы менять порядок.",
        "action": "Действие",
        "action_type": "Тип действия",
        "value_placeholder": "Значение действия",
        "browse": "Выбрать через Проводник",
        "profile": "Профиль",
        "new_profile_name": "Новый профиль",
        "save": "Сохранить",
        "cancel": "Отмена",
        "untitled": "Без названия",
        "status_ready": "Готово",
        "profile_done": "Профиль «{}» выполнен.",
        "already_running": "Профиль уже выполняется.",
        "developer": "РАЗРАБОТЧИК",
        "support": "Поддержать",
        "telegram": "Telegram",
        "donate": "Донат",
    },
    "en": {
        "profiles": "Profiles",
        "settings": "Settings",
        "new_profile": "+ NEW PROFILE",
        "run": "RUN",
        "edit": "CONFIGURE",
        "delete": "DELETE",
        "delete_confirm_title": "Delete profile?",
        "delete_confirm_text": "Profile “{}” will be permanently deleted.",
        "subtitle": "PERSONAL AUTOMATION",
        "desc": "One button — any sequence of Windows actions.",
        "actions_count": "actions",
        "no_actions": "This profile has no actions yet.",
        "confirm_title": "Confirmation",
        "confirm_power": "contains shutdown or restart.\n\nContinue?",
        "done": "Done",
        "error": "Error",
        "language": "Language",
        "autostart": "Run ONE BUTTON at Windows startup",
        "notifications": "Show notifications after run",
        "confirm_power_opt": "Confirm shutdown and restart",
        "minimize": "Minimize window after profile run",
        "save_changes": "SAVE CHANGES",
        "reset": "Reset settings",
        "saved": "Settings saved",
        "profile_setup": "Profile setup",
        "profile_name": "Name",
        "add_action": "+ Add action",
        "change": "Edit",
        "remove": "Remove",
        "drag_hint": "Drag actions to change the order.",
        "action": "Action",
        "action_type": "Action type",
        "value_placeholder": "Action value",
        "browse": "Browse",
        "profile": "Profile",
        "new_profile_name": "New profile",
        "save": "Save",
        "cancel": "Cancel",
        "untitled": "Untitled",
        "status_ready": "Done",
        "profile_done": "Profile “{}” completed.",
        "already_running": "Profile is already running.",
        "developer": "DEVELOPER",
        "support": "Support",
        "telegram": "Telegram",
        "donate": "Donate",
    },
}


def tr(lang, key):
    return TEXTS.get(lang, TEXTS["ru"]).get(key, key)


def load_data():
    APP_DIR.mkdir(parents=True, exist_ok=True)

    if not DATA_FILE.exists():
        save_data(DEFAULT_DATA)
        return json.loads(json.dumps(DEFAULT_DATA))

    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))

        if "settings" not in data or not isinstance(data["settings"], dict):
            data["settings"] = {}

        for key, value in DEFAULT_DATA["settings"].items():
            data["settings"].setdefault(key, value)

        if "profiles" not in data or not isinstance(data["profiles"], list):
            data["profiles"] = []

        for p in data["profiles"]:
            p.setdefault("accent", "#8B5CF6")
            p.setdefault("actions", [])
            p.setdefault("name", "Profile")

        return data

    except Exception:
        return json.loads(json.dumps(DEFAULT_DATA))


def save_data(data):
    APP_DIR.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def set_autostart(enabled):
    if os.name != "nt":
        return

    startup = (
        Path(os.getenv("APPDATA", ""))
        / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
    )
    startup.mkdir(parents=True, exist_ok=True)
    bat = startup / "ONE BUTTON.cmd"

    if enabled:
        if getattr(sys, "frozen", False):
            target = Path(sys.executable).resolve()
            command = f'start "" "{target}"'
        else:
            python_exe = Path(sys.executable).resolve()
            script = Path(__file__).resolve()
            pythonw = python_exe.with_name("pythonw.exe")
            if pythonw.exists():
                python_exe = pythonw
            command = f'start "" "{python_exe}" "{script}"'

        bat.write_text(command, encoding="utf-8")
    else:
        if bat.exists():
            try:
                bat.unlink()
            except Exception:
                pass


def open_default_url(url):
    if not url:
        return
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    QDesktopServices.openUrl(QUrl(url))


def _check_path(path):
    path = os.path.expandvars(os.path.expanduser(path))
    if not Path(path).exists():
        raise FileNotFoundError(f"Не найдено:\n{path}")
    return path


def launch_program(path):
    os.startfile(_check_path(path))


def open_file(path):
    os.startfile(_check_path(path))


def open_folder(path):
    os.startfile(_check_path(path))


def close_process(name):
    if not name:
        return
    if not name.lower().endswith(".exe"):
        name += ".exe"
    subprocess.run(
        ["taskkill", "/IM", name, "/F"],
        capture_output=True, text=True,
        creationflags=(subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0),
    )


def run_command(command):
    if not command:
        return
    subprocess.Popen(
        command, shell=True,
        creationflags=(subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0),
    )


ACTION_NAMES_RU = {
    "launch": "Запустить приложение",
    "website": "Открыть сайт",
    "file": "Открыть файл",
    "folder": "Открыть папку",
    "wait": "Пауза",
    "close": "Закрыть приложение",
    "command": "Команда Windows",
    "lock": "Заблокировать ПК",
    "sleep": "Спящий режим",
    "restart": "Перезагрузить ПК",
    "shutdown": "Выключить ПК",
}

ACTION_NAMES_EN = {
    "launch": "Launch application",
    "website": "Open website",
    "file": "Open file",
    "folder": "Open folder",
    "wait": "Wait",
    "close": "Close application",
    "command": "Windows command",
    "lock": "Lock PC",
    "sleep": "Sleep",
    "restart": "Restart PC",
    "shutdown": "Shut down PC",
}


def action_label(typ, value="", lang="ru"):
    names = ACTION_NAMES_RU if lang == "ru" else ACTION_NAMES_EN
    name = names.get(typ, typ)
    if value:
        if typ == "launch":
            return f"{name}: {Path(value).name}"
        return f"{name}: {value}"
    return name


class Worker(QThread):
    progress = Signal(str)
    finished_ok = Signal()
    failed = Signal(str)

    def __init__(self, actions, lang="ru"):
        super().__init__()
        self.actions = actions
        self.lang = lang

    def run(self):
        try:
            total = len(self.actions)
            for i, action in enumerate(self.actions, 1):
                typ = action.get("type")
                value = action.get("value", "")

                self.progress.emit(f"{i}/{total}   {action_label(typ, value, self.lang)}")

                if typ == "launch":
                    launch_program(value)
                elif typ == "website":
                    open_default_url(value)
                elif typ == "file":
                    open_file(value)
                elif typ == "folder":
                    open_folder(value)
                elif typ == "wait":
                    time.sleep(max(0, float(value or 0)))
                elif typ == "close":
                    close_process(value)
                elif typ == "command":
                    run_command(value)
                elif typ == "lock":
                    subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
                elif typ == "sleep":
                    subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0", "1", "0"])
                elif typ == "restart":
                    subprocess.run(["shutdown", "/r", "/t", "0"])
                elif typ == "shutdown":
                    subprocess.run(["shutdown", "/s", "/t", "0"])

            self.finished_ok.emit()
        except Exception as e:
            self.failed.emit(str(e))


class ActionDialog(QDialog):
    def __init__(self, parent=None, language="ru", existing=None):
        super().__init__(parent)
        self.language = language
        self.existing = existing or {}

        self.setWindowTitle(tr(language, "action"))
        self.setMinimumWidth(560)
        self.setWindowIcon(load_icon())

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


class DevCard(QFrame):
    def __init__(self, lang="ru"):
        super().__init__()

        self.setObjectName("DevCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(8)

        title = QLabel(tr(lang, "developer"))
        title.setObjectName("DevTitle")
        layout.addWidget(title)

        name = QLabel(DEV_NAME)
        name.setObjectName("DevName")
        layout.addWidget(name)

        tg = QPushButton(tr(lang, "telegram"))
        tg.setObjectName("DevButton")
        tg.setCursor(Qt.PointingHandCursor)
        tg.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(DEV_TELEGRAM)))
        layout.addWidget(tg)

        donate = QPushButton(f"♥  {tr(lang, 'donate')}")
        donate.setObjectName("DonateButton")
        donate.setCursor(Qt.PointingHandCursor)
        donate.setMinimumHeight(36)
        donate.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(DEV_DONATE)))
        layout.addWidget(donate)


class ProfileCard(QFrame):
    def __init__(self, profile, index, main):
        super().__init__()

        self.main = main
        self.index = index
        self.setObjectName("ProfileCard")
        self.setMinimumHeight(110)

        accent = profile.get("accent", "#8B5CF6")

        self.setStyleSheet(f"""
            #ProfileCard {{
                background: #0A0A0A;
                border: 1px solid #151515;
                border-left: 3px solid {accent};
                border-radius: 16px;
            }}
            #ProfileCard:hover {{
                background: #0F0F0F;
                border: 1px solid {accent};
                border-left: 3px solid {accent};
            }}
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(40)
        shadow.setColor(QColor(0, 0, 0, 220))
        shadow.setOffset(0, 8)
        self.setGraphicsEffect(shadow)

        lang = main.lang

        row = QHBoxLayout(self)
        row.setContentsMargins(24, 18, 18, 18)
        row.setSpacing(18)

        info = QVBoxLayout()
        info.setSpacing(4)

        name = QLabel(profile["name"])
        name.setObjectName("ProfileName")
        info.addWidget(name)

        count = QLabel(
            f"{len(profile.get('actions', []))} {tr(lang, 'actions_count')}"
        )
        count.setObjectName("Muted")
        info.addWidget(count)

        info.addStretch()
        row.addLayout(info, 1)

        buttons = QHBoxLayout()
        buttons.setSpacing(10)

        run = QPushButton(tr(lang, "run"))
        run.setObjectName("PrimaryButton")
        run.setMinimumHeight(42)
        run.setMinimumWidth(150)
        run.setCursor(Qt.PointingHandCursor)
        run.setStyleSheet(f"""
            #PrimaryButton {{
                background: {accent};
                border: 1px solid {accent};
                color: white;
                font-weight: 800;
                border-radius: 11px;
                padding: 10px 22px;
            }}
            #PrimaryButton:hover {{
                border: 1px solid white;
            }}
        """)

        edit = QPushButton(tr(lang, "edit"))
        edit.setMinimumHeight(42)
        edit.setMinimumWidth(120)
        edit.setCursor(Qt.PointingHandCursor)

        delete = QPushButton(tr(lang, "delete"))
        delete.setObjectName("DangerButton")
        delete.setMinimumHeight(42)
        delete.setMinimumWidth(110)
        delete.setCursor(Qt.PointingHandCursor)

        buttons.addWidget(run)
        buttons.addWidget(edit)
        buttons.addWidget(delete)

        row.addLayout(buttons, 0)

        run.clicked.connect(lambda: main.run_profile(index))
        edit.clicked.connect(lambda: main.edit_profile(index))
        delete.clicked.connect(lambda: main.delete_profile(index))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.data = load_data()
        self.lang = self.data["settings"].get("language", "ru")
        self.worker = None

        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(load_icon())
        self.resize(1150, 730)
        self.setMinimumSize(900, 600)

        root = QWidget()
        self.setCentralWidget(root)

        outer = QHBoxLayout(root)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(230)

        side = QVBoxLayout(sidebar)
        side.setContentsMargins(20, 26, 20, 20)
        side.setSpacing(4)

        logo = QLabel("ONE BUTTON")
        logo.setObjectName("Logo")
        side.addWidget(logo)

        sub = QLabel(tr(self.lang, "subtitle"))
        sub.setObjectName("Subtitle")
        side.addWidget(sub)

        side.addSpacing(30)

        self.home_btn = QPushButton(f"  ▦   {tr(self.lang, 'profiles')}")
        self.settings_btn = QPushButton(f"  ⚙   {tr(self.lang, 'settings')}")
        for b in (self.home_btn, self.settings_btn):
            b.setObjectName("NavButton")
            b.setMinimumHeight(46)
            b.setCursor(Qt.PointingHandCursor)

        side.addWidget(self.home_btn)
        side.addWidget(self.settings_btn)
        side.addStretch()

        self.dev_card = DevCard(self.lang)
        side.addWidget(self.dev_card)

        side.addSpacing(10)

        version = QLabel("v1.0")
        version.setObjectName("Muted")
        version.setAlignment(Qt.AlignCenter)
        side.addWidget(version)

        outer.addWidget(sidebar)

        self.stack = QStackedWidget()
        outer.addWidget(self.stack)

        self.home = QWidget()
        self.home_layout = QVBoxLayout(self.home)
        self.home_layout.setContentsMargins(40, 34, 40, 34)
        self.home_layout.setSpacing(14)
        self.stack.addWidget(self.home)

        self.settings_page = SettingsPage(self.data)
        self.stack.addWidget(self.settings_page)

        self.home_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.settings_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        self.settings_page.changed.connect(self.on_settings_changed)

        self.statusBar().showMessage(tr(self.lang, "status_ready"))

        self.refresh()

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()
                continue
            child = item.layout()
            if child is not None:
                self._clear_layout(child)
                child.deleteLater()

    def on_settings_changed(self):
        self.lang = self.data["settings"].get("language", "ru")
        self._relang()
        self.refresh()

    def _relang(self):
        self.home_btn.setText(f"  ▦   {tr(self.lang, 'profiles')}")
        self.settings_btn.setText(f"  ⚙   {tr(self.lang, 'settings')}")
        self.statusBar().showMessage(tr(self.lang, "status_ready"))

        if hasattr(self, "dev_card") and self.dev_card is not None:
            new_card = DevCard(self.lang)
            sidebar_layout = self.dev_card.parentWidget().layout()
            sidebar_layout.replaceWidget(self.dev_card, new_card)
            self.dev_card.deleteLater()
            self.dev_card = new_card

    def refresh(self):
        self._clear_layout(self.home_layout)

        top = QHBoxLayout()
        title = QLabel(tr(self.lang, "profiles"))
        title.setObjectName("PageTitle")
        top.addWidget(title)
        top.addStretch()

        add = QPushButton(tr(self.lang, "new_profile"))
        add.setObjectName("PrimaryButton")
        add.setMinimumHeight(44)
        add.setCursor(Qt.PointingHandCursor)
        add.clicked.connect(self.add_profile)
        top.addWidget(add)

        self.home_layout.addLayout(top)

        desc = QLabel(tr(self.lang, "desc"))
        desc.setObjectName("Muted")
        self.home_layout.addWidget(desc)

        self.home_layout.addSpacing(10)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        container = QWidget()
        grid = QVBoxLayout(container)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(16)

        for i, profile in enumerate(self.data["profiles"]):
            grid.addWidget(ProfileCard(profile, i, self))

        grid.addStretch()
        scroll.setWidget(container)

        self.home_layout.addWidget(scroll)

    def add_profile(self):
        dialog = QDialog(self)
        dialog.setWindowTitle(tr(self.lang, "profile"))
        dialog.setMinimumWidth(440)
        dialog.setWindowIcon(load_icon())

        form = QFormLayout(dialog)
        form.setContentsMargins(24, 24, 24, 24)
        form.setSpacing(12)

        name = QLineEdit(tr(self.lang, "new_profile_name"))
        form.addRow(tr(self.lang, "profile_name"), name)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText(tr(self.lang, "save"))
        buttons.button(QDialogButtonBox.Cancel).setText(tr(self.lang, "cancel"))
        form.addRow(buttons)

        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        if dialog.exec():
            accents = ["#8B5CF6", "#A855F7", "#C084FC", "#7C3AED", "#6366F1", "#EC4899"]
            new_profile = {
                "name": name.text().strip() or tr(self.lang, "untitled"),
                "accent": accents[len(self.data["profiles"]) % len(accents)],
                "actions": [],
            }
            self.data["profiles"].append(new_profile)
            save_data(self.data)
            self.refresh()

    def delete_profile(self, index):
        if index < 0 or index >= len(self.data["profiles"]):
            return

        profile = self.data["profiles"][index]

        answer = QMessageBox.warning(
            self,
            tr(self.lang, "delete_confirm_title"),
            tr(self.lang, "delete_confirm_text").format(profile["name"]),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if answer != QMessageBox.Yes:
            return

        self.data["profiles"].pop(index)
        save_data(self.data)
        self.refresh()

    def edit_profile(self, index):
        profile = self.data["profiles"][index]

        dialog = QDialog(self)
        dialog.setWindowTitle(f"{tr(self.lang, 'profile_setup')}: {profile['name']}")
        dialog.resize(680, 620)
        dialog.setWindowIcon(load_icon())

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        top = QHBoxLayout()
        name = QLineEdit(profile["name"])
        top.addWidget(QLabel(tr(self.lang, "profile_name")))
        top.addWidget(name)
        layout.addLayout(top)

        actions = QListWidget()
        actions.setDragDropMode(QListWidget.InternalMove)
        layout.addWidget(actions)

        def rebuild():
            actions.clear()
            for action in profile.get("actions", []):
                item = QListWidgetItem(
                    action_label(action["type"], action.get("value", ""), self.lang)
                )
                item.setData(Qt.UserRole, action)
                actions.addItem(item)

        rebuild()

        controls = QHBoxLayout()
        add = QPushButton(tr(self.lang, "add_action"))
        edit = QPushButton(tr(self.lang, "change"))
        remove = QPushButton(tr(self.lang, "remove"))
        controls.addWidget(add)
        controls.addWidget(edit)
        controls.addWidget(remove)
        layout.addLayout(controls)

        def add_action():
            d = ActionDialog(dialog, self.lang)
            if d.exec():
                profile["actions"].append(d.result_action())
                rebuild()

        def edit_action():
            row = actions.currentRow()
            if row < 0:
                return
            d = ActionDialog(dialog, self.lang, profile["actions"][row])
            if d.exec():
                profile["actions"][row] = d.result_action()
                rebuild()

        def remove_action():
            row = actions.currentRow()
            if row >= 0:
                profile["actions"].pop(row)
                rebuild()

        add.clicked.connect(add_action)
        edit.clicked.connect(edit_action)
        remove.clicked.connect(remove_action)

        info = QLabel(tr(self.lang, "drag_hint"))
        info.setObjectName("Muted")
        layout.addWidget(info)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Save).setText(tr(self.lang, "save"))
        buttons.button(QDialogButtonBox.Cancel).setText(tr(self.lang, "cancel"))
        layout.addWidget(buttons)

        def save():
            profile["name"] = name.text().strip() or tr(self.lang, "untitled")
            profile["actions"] = [
                actions.item(i).data(Qt.UserRole) for i in range(actions.count())
            ]
            save_data(self.data)
            dialog.accept()

        buttons.accepted.connect(save)
        buttons.rejected.connect(dialog.reject)

        dialog.exec()
        self.refresh()

    def run_profile(self, index):
        if self.worker is not None and self.worker.isRunning():
            QMessageBox.information(
                self, APP_NAME, tr(self.lang, "already_running")
            )
            return

        profile = self.data["profiles"][index]
        actions = profile.get("actions", [])

        if not actions:
            QMessageBox.information(self, APP_NAME, tr(self.lang, "no_actions"))
            return

        dangerous = any(a["type"] in ("shutdown", "restart") for a in actions)

        if dangerous and self.data["settings"].get("confirm_power", True):
            answer = QMessageBox.warning(
                self,
                tr(self.lang, "confirm_title"),
                f'«{profile["name"]}» {tr(self.lang, "confirm_power")}',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if answer != QMessageBox.Yes:
                return

        self.worker = Worker(actions, self.lang)
        self.worker.progress.connect(self.show_status)
        self.worker.finished_ok.connect(lambda: self.run_finished(profile["name"]))
        self.worker.failed.connect(self.run_failed)
        self.worker.start()

    def show_status(self, text):
        self.statusBar().showMessage(text)

    def run_finished(self, name):
        self.statusBar().showMessage(f"{tr(self.lang, 'done')}: {name}")

        if self.data["settings"].get("notifications", True):
            self.statusBar().showMessage(tr(self.lang, "profile_done").format(name))

        if self.data["settings"].get("minimize_after_run", False):
            self.showMinimized()

    def run_failed(self, error):
        QMessageBox.critical(self, tr(self.lang, "error"), error)
        self.statusBar().clearMessage()


APP_STYLE = """
QMainWindow, QWidget {
    background: #000000;
    color: #EDEDED;
    font-family: "Segoe UI";
    font-size: 14px;
}

QToolTip {
    background: #0A0A0A;
    color: #EDEDED;
    border: 1px solid #1A1A1A;
    padding: 6px;
    border-radius: 6px;
}

QLabel {
    background: transparent;
    border: none;
}

#Sidebar {
    background: #050505;
    border-right: 1px solid #111111;
}

#Logo {
    font-size: 22px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #FFFFFF;
}

#Subtitle {
    color: #4A4A4A;
    font-size: 9px;
    letter-spacing: 2px;
}

#PageTitle {
    font-size: 30px;
    font-weight: 800;
    color: #FFFFFF;
}

#Muted {
    color: #5A5A5A;
}

QPushButton {
    background: #0A0A0A;
    border: 1px solid #1A1A1A;
    border-radius: 11px;
    padding: 10px 16px;
    color: #DADADA;
    font-weight: 600;
}

QPushButton:hover {
    background: #141414;
    border: 1px solid #8B5CF6;
    color: #FFFFFF;
}

QPushButton:pressed {
    background: #1A1A1A;
}

#PrimaryButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #6D28D9, stop:1 #A855F7);
    border: 1px solid #7C3AED;
    color: #FFFFFF;
    font-weight: 800;
    border-radius: 11px;
    padding: 10px 18px;
}

#PrimaryButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                stop:0 #7C3AED, stop:1 #C084FC);
    border: 1px solid #A970FF;
}

#PrimaryButton:pressed {
    background: #6D28D9;
}

#DangerButton {
    background: #1A0A0A;
    border: 1px solid #3A1414;
    color: #E88A8A;
    font-weight: 700;
    border-radius: 11px;
    padding: 10px 18px;
}

#DangerButton:hover {
    background: #2A0F0F;
    border: 1px solid #EF4444;
    color: #FFFFFF;
}

#DangerButton:pressed {
    background: #3A1414;
}

#NavButton {
    text-align: left;
    background: transparent;
    border: 1px solid transparent;
    padding: 13px 15px;
    border-radius: 11px;
    color: #8A8A8A;
    font-weight: 600;
}

#NavButton:hover {
    background: #0A0A0A;
    border-color: #1A1A1A;
    color: #FFFFFF;
}

#ProfileCard,
#Card {
    background: #0A0A0A;
    border: 1px solid #151515;
    border-radius: 16px;
}

#ProfileName {
    font-size: 20px;
    font-weight: 800;
    color: #FFFFFF;
}

QLineEdit,
QComboBox {
    background: #050505;
    border: 1px solid #151515;
    border-radius: 10px;
    padding: 10px 12px;
    color: #EDEDED;
    selection-background-color: #7C3AED;
}

QLineEdit:focus,
QComboBox:focus {
    border: 1px solid #8B5CF6;
    background: #0A0A0A;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox QAbstractItemView {
    background: #050505;
    border: 1px solid #1A1A1A;
    selection-background-color: #7C3AED;
    color: #EDEDED;
    outline: none;
}

QListWidget {
    background: #050505;
    border: 1px solid #151515;
    border-radius: 12px;
    padding: 8px;
}

QListWidget::item {
    background: #0A0A0A;
    border: 1px solid #151515;
    border-radius: 10px;
    padding: 13px;
    margin: 4px;
    color: #DADADA;
}

QListWidget::item:selected {
    background: #141414;
    border: 1px solid #8B5CF6;
    color: #FFFFFF;
}

QCheckBox {
    spacing: 10px;
    padding: 8px;
    color: #B8B8B8;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 5px;
    border: 1px solid #1F1F1F;
    background: #050505;
}

QCheckBox::indicator:hover {
    border: 1px solid #8B5CF6;
}

QCheckBox::indicator:checked {
    background: #8B5CF6;
    border: 1px solid #A970FF;
}

QScrollArea {
    border: none;
    background: transparent;
}

QScrollBar:vertical {
    background: transparent;
    width: 10px;
    margin: 4px;
}

QScrollBar::handle:vertical {
    background: #1A1A1A;
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: #7C3AED;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background: transparent;
    height: 10px;
    margin: 4px;
}

QScrollBar::handle:horizontal {
    background: #1A1A1A;
    border-radius: 5px;
    min-width: 30px;
}

QStatusBar {
    background: #050505;
    color: #6A6A6A;
    border-top: 1px solid #111111;
}

QStatusBar::item {
    border: none;
}

QDialog {
    background: #000000;
}

QDialogButtonBox QPushButton {
    min-width: 110px;
    padding: 9px 16px;
}

QMessageBox {
    background: #000000;
}

QMessageBox QLabel {
    color: #EDEDED;
}

#DevCard {
    background: #0A0A0A;
    border: 1px solid #151515;
    border-radius: 14px;
}

#DevTitle {
    color: #5A5A5A;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
}

#DevName {
    color: #FFFFFF;
    font-size: 16px;
    font-weight: 800;
    letter-spacing: 1px;
}

#DevButton {
    background: #0F0F0F;
    border: 1px solid #1A1A1A;
    border-radius: 9px;
    padding: 7px 10px;
    color: #B8B8B8;
    font-weight: 600;
    font-size: 12px;
}

#DevButton:hover {
    background: #141414;
    border: 1px solid #8B5CF6;
    color: #FFFFFF;
}

#DonateButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #6D28D9, stop:1 #A855F7);
    border: 1px solid #7C3AED;
    border-radius: 10px;
    color: #FFFFFF;
    font-weight: 800;
    font-size: 12px;
    padding: 8px 12px;
}

#DonateButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #7C3AED, stop:1 #C084FC);
    border: 1px solid #A970FF;
}
"""


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setWindowIcon(load_icon())
    app.setStyleSheet(APP_STYLE)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()