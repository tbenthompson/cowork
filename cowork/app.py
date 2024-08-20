import sys
from PyQt6.QtWidgets import (
    QApplication,
    QSystemTrayIcon,
    QMenu,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QInputDialog,
)
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QTimer, QTime, Qt

reminder_times = []
popups = []
early_check_in = False
tray_icon = None
last_reminder_minute = -1  # Add this line


def setup_tray():
    global tray_icon
    tray_icon = QSystemTrayIcon()
    tray_icon.setIcon(QIcon.fromTheme("clock"))

    tray_menu = QMenu()
    set_early_action = QAction("Set Early", tray_icon)
    set_early_action.triggered.connect(set_early_check_in)
    tray_menu.addAction(set_early_action)

    quit_action = tray_menu.addAction("Quit")
    quit_action.triggered.connect(QApplication.instance().quit)

    tray_icon.setContextMenu(tray_menu)
    tray_icon.show()


def set_early_check_in():
    global early_check_in
    early_check_in = True


def check_time():
    global early_check_in, last_reminder_minute
    current_time = QTime.currentTime()
    current_minute = current_time.minute()

    # Reset last_reminder_minute when crossing the hour boundary
    if current_minute == 0:
        last_reminder_minute = -1

    if early_check_in:
        next_reminder = min(
            (t for t in reminder_times if t > current_minute),
            default=reminder_times[0],
        )
        if (
            next_reminder - 2
        ) % 60 == current_minute and current_minute != last_reminder_minute:
            show_reminder()
            early_check_in = False
            last_reminder_minute = current_minute

    if (
        current_minute in reminder_times
        and not popups
        and current_minute != last_reminder_minute
    ):
        show_reminder()
        last_reminder_minute = current_minute


def show_reminder():
    for screen in QApplication.screens():
        popup = ReminderPopup(close_popups)
        popup.move(screen.geometry().center() - popup.rect().center())
        popup.show()
        popups.append(popup)


def close_popups():
    for popup in popups:
        popup.close()
    popups.clear()


def prompt_for_reminder_times():
    times, ok = QInputDialog.getText(
        None,
        "Enter reminder times",
        "Enter comma-separated minute values (e.g., 00,15,30,45):",
    )
    if ok:
        global reminder_times
        reminder_times = [
            int(t.strip()) for t in times.split(",") if t.strip().isdigit()
        ]
    else:
        QApplication.instance().quit()
    return ok


class ReminderPopup(QWidget):
    def __init__(self, close_callback):
        super().__init__()
        self.close_callback = close_callback
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Reminder")
        self.setGeometry(100, 100, 300, 200)
        layout = QVBoxLayout()

        label = QLabel("Reminder: Time to check in!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.on_ok_clicked)
        quit_button = QPushButton("Quit")
        quit_button.clicked.connect(QApplication.instance().quit)

        button_layout.addWidget(ok_button)
        button_layout.addWidget(quit_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def on_ok_clicked(self):
        self.close()
        self.close_callback()

    def closeEvent(self, event):
        self.on_ok_clicked()
        event.accept()


def main():
    app = QApplication(sys.argv)

    # Prevent the app from quitting when the last window is closed
    app.setQuitOnLastWindowClosed(False)

    if not prompt_for_reminder_times():
        return 0

    setup_tray()

    timer = QTimer()
    timer.timeout.connect(check_time)
    timer.start(1000)  # Check every second

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
