import os
import webview
import pystray
from PIL import Image
import threading
import keyboard
import time
import pyaudio
import wave
import queue
from openai import OpenAI
from io import BytesIO
import pyperclip
import sys

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def create_colored_icon(color):
    return Image.new('RGB', (64, 64), color=color)

class Api:
    def __init__(self, window):
        self.window = window
        self.is_visible = True
        self.is_recording = False
        self.recording_thread = None
        self.audio_queue = queue.Queue()
        self.selected_language = "en"
        self.tray_icon = None
        self.last_transcription = ""
        
        self.languages = {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese",
            "nl": "Dutch",
            "pl": "Polish",
            "ru": "Russian",
            "zh": "Chinese",
            "ja": "Japanese",
            "ko": "Korean"
        }

    def minimize_to_tray(self):
        self.window.hide()
        self.is_visible = False

    def toggle_window(self):
        if self.is_visible:
            self.window.hide()
            self.is_visible = False
        else:
            self.window.show()
            self.is_visible = True
            
    def set_language(self, lang_code):
        if lang_code in self.languages:
            self.selected_language = lang_code
            return {"status": "success", "language": self.languages[lang_code]}
        return {"status": "error", "message": "Invalid language code"}
    
    def get_languages(self):
        return self.languages

    def update_icon(self, color):
        if self.tray_icon:
            self.tray_icon.icon = create_colored_icon(color)

    def copy_last_transcription(self):
        if self.last_transcription:
            pyperclip.copy(self.last_transcription)
            return True
        return False

def create_wav_buffer(audio_data):
    wav_buffer = BytesIO()
    with wave.open(wav_buffer, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(44100)
        wf.writeframes(b''.join(audio_data))
    wav_buffer.seek(0)
    return wav_buffer

def type_text(text):
    time.sleep(0.5)
    keyboard.write(text)

def transcribe_audio(audio_data, api):
    try:
        api.update_icon('blue')
        wav_buffer = create_wav_buffer(audio_data)
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=("audio.wav", wav_buffer),
            language=api.selected_language
        )
        
        text = transcript.text
        api.last_transcription = text
        print(f"Transcription ({api.languages[api.selected_language]}): {text}")
        type_text(text)
        return text
        
    except Exception as e:
        print(f"Error during transcription: {e}")
        return f"Error: {str(e)}"
    finally:
        if wav_buffer:
            wav_buffer.close()
        api.update_icon('red')

def record_audio(api):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    
    p = pyaudio.PyAudio()
    recorded_frames = []
    
    try:
        print(f"Recording started... (Language: {api.languages[api.selected_language]})")
        api.update_icon('green')
        
        stream = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       input=True,
                       frames_per_buffer=CHUNK)
        
        while api.is_recording:
            data = stream.read(CHUNK, exception_on_overflow=False)
            recorded_frames.append(data)
        
        print("Recording stopped, transcribing...")
        
        stream.stop_stream()
        stream.close()
        
        if recorded_frames:
            transcribe_audio(recorded_frames, api)
            
    except Exception as e:
        print(f"Error during recording: {e}")
        api.update_icon('red')
    finally:
        p.terminate()
        api.is_recording = False

def handle_keyboard(api):
    key_press_start = 0
    
    while True:
        if keyboard.is_pressed('ctrl+space'):
            if key_press_start == 0:
                key_press_start = time.time()
            elif time.time() - key_press_start >= 0.3 and not api.is_recording:
                api.is_recording = True
                api.recording_thread = threading.Thread(target=record_audio, args=(api,))
                api.recording_thread.start()
                print("Started recording!")
                time.sleep(0.1)
        else:
            if key_press_start != 0:
                if api.is_recording:
                    api.is_recording = False
                    if api.recording_thread:
                        api.recording_thread.join()
                        print("Stopped recording!")
                key_press_start = 0
            time.sleep(0.1)

def create_tray_icon(window, api):
    icon_image = create_colored_icon('red')
    
    def on_clicked(icon, item):
        if str(item) == "Show/Hide":
            api.toggle_window()
        elif str(item) == "Copy Last":
            if api.copy_last_transcription():
                print("Last transcription copied to clipboard")
            else:
                print("No transcription available to copy")
        elif str(item) == "Exit":
            if api.is_recording:
                api.is_recording = False
                if api.recording_thread:
                    api.recording_thread.join()
            icon.stop()
            os._exit(0)

    def on_activate(icon):
        api.toggle_window()

    menu = (
        pystray.MenuItem("Show/Hide", on_clicked),
        pystray.MenuItem("Copy Last", on_clicked),
        pystray.MenuItem("Exit", on_clicked)
    )
    
    icon = pystray.Icon(
        "name",
        icon_image,
        "Voice Recorder (Hold Ctrl+Space)",
        menu
    )
    
    icon.on_activate = on_activate
    api.tray_icon = icon
    return icon

def main():
    api = Api(None)
    
    window = webview.create_window(
        'Voice Recorder',
        url=get_resource_path(os.path.join('templates', 'index.html')),
        width=400,
        height=500,
        resizable=False,
        text_select=False,
        frameless=True,
        js_api=api,
        hidden=False
    )
    
    api.window = window
    
    keyboard_thread = threading.Thread(target=handle_keyboard, args=(api,), daemon=True)
    keyboard_thread.start()
    
    icon = create_tray_icon(window, api)
    tray_thread = threading.Thread(target=icon.run)
    tray_thread.daemon = True
    tray_thread.start()
    
    webview.start()

if __name__ == '__main__':
    main()