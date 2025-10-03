import speech_recognition as sr
from pydub import AudioSegment
import os

def transcribe_audio(file_path):
    # Convert MP3 to WAV if necessary
    if file_path.lower().endswith('.mp3'):
        wav_path = file_path.rsplit('.', 1)[0] + '_converted.wav'
        audio = AudioSegment.from_mp3(file_path)
        audio.export(wav_path, format='wav')
        file_to_use = wav_path
    else:
        file_to_use = file_path

    recognizer = sr.Recognizer()
    with sr.AudioFile(file_to_use) as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        text = "Could not understand audio"
    except sr.RequestError:
        text = "Could not request results from the speech recognition service"
    finally:
        # Clean up converted file
        if file_path.lower().endswith('.mp3') and os.path.exists(wav_path):
            os.remove(wav_path)

    return text
