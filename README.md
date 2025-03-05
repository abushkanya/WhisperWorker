# WhisperWorker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight desktop application for real-time voice transcription using OpenAI's Whisper API. Features a system tray interface and global hotkey support.

## Features

- Real-time voice recording and transcription
- Multi-language support (12 languages)
- System tray integration with status indicators:
  - Red: Idle
  - Green: Recording
  - Blue: Processing
- Global hotkey (Ctrl+Space) for recording
- Clipboard history for last transcription
- Minimalistic, frameless UI
- Auto-insertion of transcribed text at cursor position

## Supported Languages

- English
- Spanish
- French
- German
- Italian
- Portuguese
- Dutch
- Polish
- Russian
- Chinese
- Japanese
- Korean

## Requirements

- Windows 10/11
- Microphone
- OpenAI API Key
- Internet connection

## Installation

### Option 1: Run from Source

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the application:
```bash
python main.py
```

### Option 2: Executable

1. Run `build.bat`
2. Find `WhisperWorker.exe` in the `dist` folder
3. Run the executable

> **Note:** You should use your own OpenAI API key for the application to function properly. You can obtain an API key by signing up at [OpenAI's website](https://openai.com/).

## Usage

1. Launch the application
2. Select your preferred language from the dropdown
3. Hold Ctrl+Space to start recording
4. Release to stop and transcribe
5. Text will appear at your cursor position
6. Access last transcription from tray icon menu

## System Tray Features

- Show/Hide: Toggle main window
- Copy Last: Copy last transcription to clipboard
- Exit: Close application

## Building

To create a standalone executable for Windows:
```bash
build.bat
```
The executable will be created in the `dist` folder.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 