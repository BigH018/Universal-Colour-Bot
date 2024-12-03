# TriggerBot with GUI

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![PyQt5](https://img.shields.io/badge/PyQt5-v5.15-orange)

## Overview

TriggerBot is an automated color detection tool designed to perform specific actions when a defined color is detected on your screen. The project integrates a powerful PyQt5-based graphical user interface (GUI) to make configuration user-friendly and highly customizable.

Key features include:
- Color-based automation with adjustable RGB and tolerance settings.
- Hotkey support for activation, including custom key bindings.
- Adjustable timing settings for precise control.
- Toggleable dark/light mode for user preference.
- Detailed built-in tutorial for quick onboarding.

---

## Features

### 🔑 **Hotkey Settings**
- Choose from predefined hotkeys or specify custom ones using hexadecimal codes.
- Hotkeys can be configured to activate or toggle the bot.

### 🎨 **Color Detection Settings**
- Define target colors using RGB values.
- Adjustable color tolerance for fine-grained detection control.

### ⏳ **Timing Settings**
- Set delays for trigger actions with percentage-based and base delays.

### 🌗 **Dark/Light Mode**
- Switch between visually appealing dark and light themes.

### 📚 **Built-In Tutorial**
- A multi-page, interactive tutorial explains the bot's features and usage in detail.

### 🛠️ **Emergency Exit**
- Quickly terminate the bot using a keyboard shortcut (`Ctrl+Shift+X`).

---

## Prerequisites
- **Python 3.8+**
- The following Python libraries:
  - `PyQt5`
  - `keyboard`
  - `numpy`
  - `mss`
  - `pywin32`

---

## Usage

1. **Configure the Bot via GUI:**
   - Launch the program to open the settings window.
   - Set your desired color detection, timing, and hotkey settings.
   - Save your configuration.

2. **Activate the Bot:**
   - Press the designated hotkey (e.g., `F10` or a custom key) to toggle the bot on/off.
   - The bot will search for the specified color and perform actions when detected.

3. **Emergency Exit:**
   - Press `Ctrl+Shift+X` to immediately terminate the program.

---

## Files and Structure

### `gui.py`
Defines the PyQt5-based GUI for configuring bot settings. Includes:
- Dark/Light mode toggle.
- Input fields for RGB values, delays, and hotkeys.
- Interactive tutorial to guide new users.

### `main.py`
The entry point of the application. Responsibilities:
- Initializes the bot (`triggerbot`) and GUI.
- Runs the bot's logic in a separate thread to ensure concurrency.

### `TriggerBot.py`
Implements the core bot functionality:
- Color detection using screen capture.
- Hotkey handling for activation.
- Action triggering based on detected colors.

---

## Configuration

### Default Settings
- **Hotkey**: `Delete` (`0x02`)
- **RGB Color**: `(255, 51, 255)` (Purple)
- **Base Delay**: `0.01 seconds`
- **Trigger Delay**: `40%`
- **Color Tolerance**: `70`

All settings can be adjusted via the GUI.

---

## Screenshots

### Light-Mode :nauseated_face: :vomiting_face:
![Main Settings](https://github.com/user-attachments/assets/cb9492c6-b1d5-4719-a834-22c2c0d36a66)

### Dark-Mode
![Tutorial Page](https://github.com/user-attachments/assets/06b30e9d-b2ba-458c-8aa8-f12643f39113) 

### Tutorial
![Window Title](https://github.com/user-attachments/assets/9566853a-3e29-4bae-b6e5-3249bc189af6)

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Disclaimer

This tool is for educational purposes only. Use it responsibly.
