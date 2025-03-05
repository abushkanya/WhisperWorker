@echo off
pip install -r requirements.txt
pyinstaller --noconfirm --onefile --windowed ^
    --add-data "templates/index.html;templates" ^
    --hidden-import webview ^
    --hidden-import PIL ^
    --hidden-import pystray ^
    --hidden-import keyboard ^
    --hidden-import pyaudio ^
    --hidden-import wave ^
    --hidden-import openai ^
    --hidden-import pyperclip ^
    --hidden-import json ^
    --hidden-import queue ^
    --hidden-import threading ^
    --collect-data webview ^
    --name "WhisperWorker" ^
    --icon "NONE" ^
    --clean ^
    main.py
pause 