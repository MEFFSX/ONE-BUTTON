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

