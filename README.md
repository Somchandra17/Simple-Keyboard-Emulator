# Simple Keyboard Emulator

A modern GUI keyboard emulator that simulates typing with customizable speed and delay settings.

## Features

- Simulate keyboard input with realistic typing speeds
- Adjustable start delay and typing speed
- Paste from clipboard
- Save/Load text files
- Character counter
- Dark themed modern UI with platform-native fonts
- Cross-platform support (Windows, macOS, Linux)
- Fail-safe mechanism (move mouse to corner to stop)
- Persistent settings (remembers your preferences)
- Keyboard shortcuts

## Requirements

- Python 3.7+
- Tkinter (usually included with Python)
- PyAutoGUI

## Installation

1. Clone or download the repository:
   ```shell
   git clone https://github.com/Somchandra17/Simple-Keyboard-Emulator.git
   cd Simple-Keyboard-Emulator
   ```

2. Install dependencies:
   ```shell
   pip install -r requirements.txt
   ```

## Quick Start

### Windows
Double-click `run.bat` or run:
```cmd
python keyboard.py
```

### macOS
Double-click `run.command` (may need to make executable first: `chmod +x run.command`) or run:
```shell
python3 keyboard.py
```

### Linux
Run the launcher script:
```shell
chmod +x run.sh
./run.sh
```
Or directly:
```shell
python3 keyboard.py
```

## Usage

1. Enter or paste text into the text area.

2. Adjust settings:
   - **Start Delay**: Time before typing begins (0-30 seconds)
   - **Typing Speed**: Interval between characters (0.01-1.0 seconds)

3. Click **Start Typing** to begin. Switch to your target application during the countdown.

4. Click **Paste** to insert clipboard content.

5. Click **Save** to save text to a file, or **Load** to import from a file.

6. Click **Clear** to reset the text area.

## Keyboard Shortcuts

| Action | Windows/Linux | macOS |
|--------|--------------|-------|
| Start Typing | Ctrl + Enter | Cmd + Enter |
| Clear Text | Ctrl + D | Cmd + D |

## Platform-Specific Notes

### macOS Permissions
PyAutoGUI requires Accessibility permissions on macOS:
1. Open **System Settings** > **Privacy & Security** > **Accessibility**
2. Enable your terminal app (Terminal.app, iTerm2, VS Code, etc.)
3. Restart the application

### Linux
May require `python3-tk` package:
```shell
sudo apt install python3-tk
```

### Windows
If Python is not in your PATH, use the full path:
```cmd
"C:\Python3\python.exe" keyboard.py
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Typing not working | Grant Accessibility permissions (macOS) |
| Module not found error | Run `pip install -r requirements.txt` |
| Tkinter not found | Install `python3-tk` (Linux) or use official Python installer (Windows) |
| Typing too fast/slow | Adjust the "Typing Speed" setting |

## License

MIT License - see [LICENSE](LICENSE) for details.
