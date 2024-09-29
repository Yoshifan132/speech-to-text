import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import sounddevice as sd
import numpy as np

def recognize_speech():
    fs = 16000  # サンプリング周波数
    duration = 5  # 録音時間（秒）

    status_label.config(text="録音中...")
    root.update()

    # 録音
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()

    # numpy配列をAudioDataに変換
    audio_data = sr.AudioData(recording.tobytes(), fs, 2)

    # 音声認識
    r = sr.Recognizer()
    try:
        text = r.recognize_google(audio_data, language='ja-JP')
        text_area.insert(tk.END, text + '\n')
        status_label.config(text="認識成功")
    except sr.UnknownValueError:
        status_label.config(text="音声を認識できませんでした。")
    except sr.RequestError as e:
        status_label.config(text=f"サービスに接続できませんでした。; {e}")

# GUI部分は同じ
root = tk.Tk()
root.title("音声認識アプリ")

recognize_button = tk.Button(root, text="音声認識開始", command=recognize_speech)
recognize_button.pack()

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
text_area.pack()

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()