from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QPushButton, QStackedWidget, QScrollArea, QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QListWidget, QListWidgetItem, QMessageBox
from .config import APP_NAME, DEFAULT_DATA, tr, load_data, save_data
from .worker import Worker
from .dialogs import ActionDialog
from .settings import SettingsPage
from .widgets import DevCard, ProfileCard

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.data = load_data()
        self.lang = self.data["settings"].get("language", "ru")
        self.worker = None

        self.setWindowTitle(APP_NAME)
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

