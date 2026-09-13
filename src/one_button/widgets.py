from pathlib import Path
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QColor, QDesktopServices
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QGraphicsDropShadowEffect
from .config import DEV_NAME, DEV_TELEGRAM, DEV_DONATE, tr

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

