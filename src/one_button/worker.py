import subprocess
import time
from PySide6.QtCore import QThread, Signal
from .config import action_label, launch_program, open_default_url, open_file, open_folder, close_process, run_command

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

