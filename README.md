# Cowork Reminder

A simple coworking reminder app that sits in your system tray and reminds you to check in at specified times.

## Installation

This project uses Poetry for dependency management. If you don't have Poetry installed, you can install it by following the instructions at https://python-poetry.org/docs/#installation

Once Poetry is installed, you can install this app by running:

```
poetry install
```

## Usage

After installation, you can run the app by typing `cowork` in your terminal.

When first started, the app will prompt you to enter reminder times. Enter comma-separated minute values (e.g., 00,15,30,45).

The app will then sit in your system tray. At the specified times, it will show a reminder popup on all your screens.

To quit the app, right-click on the system tray icon and select "Quit".