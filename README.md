# ONE BUTTON

Personal Windows automation app built with Python and PySide6.

## Features

- Profiles with custom action sequences
- Launch applications, websites, files and folders
- Wait, close processes and run Windows commands
- Lock, sleep, restart and shut down Windows
- Russian / English interface
- Windows autostart option
- Dark black + neon purple UI
- Persistent settings and profiles

## Run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Project structure

```text
ONE BUTTON/
├── .github/
│   └── workflows/
├── assets/
├── docs/
├── src/
│   └── one_button/
│       ├── app.py
│       ├── config.py
│       ├── dialogs.py
│       ├── settings.py
│       ├── style.py
│       ├── widgets.py
│       ├── window.py
│       ├── worker.py
│       └── __init__.py
├── .gitignore
├── LICENSE
├── README.md
├── main.py
└── requirements.txt
```
