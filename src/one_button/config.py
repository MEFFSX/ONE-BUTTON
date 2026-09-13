import sys
import os
import json
import subprocess
import time
from pathlib import Path

from PySide6.QtCore import Qt, QThread, Signal, QUrl
from PySide6.QtGui import QColor, QDesktopServices
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QListWidget, QListWidgetItem, QStackedWidget,
    QLineEdit, QFileDialog, QMessageBox, QComboBox, QCheckBox, QDialog,
    QDialogButtonBox, QFrame, QScrollArea, QFormLayout, QGraphicsDropShadowEffect,
)

APP_NAME = "ONE BUTTON"

APP_DIR = Path(os.getenv("APPDATA", str(Path.home()))) / "OneButton"
DATA_FILE = APP_DIR / "data.json"

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

DEV_NAME = "MEFF¹"
DEV_TELEGRAM = "https://t.me/meffsnos"
DEV_DONATE = ""


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

