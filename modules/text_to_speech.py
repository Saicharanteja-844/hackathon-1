from gtts import gTTS
import os

def text_to_speech(text):
    audio_file = "static/audio/output.mp3"
    tts = gTTS(text=text, lang='en')
    tts.save(audio_file)
    return audio_file
