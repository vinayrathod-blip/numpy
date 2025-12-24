from gtts import gTTS
import os

def speak_gu(text: str):
    print(f"[VOICE-GUJARATI]: {text}")
    tts = gTTS(text=text, lang="gu")
    tts.save("output.mp3")
    os.system("start output.mp3")
