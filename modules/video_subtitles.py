#
import speech_recognition as sr
import os
# --- CHANGE 1: The way we import from moviepy ---
from moviepy import VideoFileClip

def generate_subtitles(video_path):
    # --- CHANGE 2: How we call the function ---
    video = VideoFileClip(video_path)
    audio_path = "temp_audio.wav"
    video.audio.write_audiofile(audio_path)

    # Close the video file to release the lock on the file
    video.close()

    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        text = "Could not understand audio"
    except sr.RequestError:
        text = "Could not request results from the speech recognition service"

    subtitle_srt_path = "static/subtitles/subtitles.srt"
    subtitle_txt_path = "static/subtitles/subtitles.txt"
    if not os.path.exists("static/subtitles"):
        os.makedirs("static/subtitles")

    # Generate SRT format
    with open(subtitle_srt_path, "w", encoding="utf-8") as f:
        f.write("1\n00:00:00,000 --> 00:00:10,000\n")
        f.write(text + "\n")

    # Generate TXT format with plain text
    with open(subtitle_txt_path, "w", encoding="utf-8") as f:
        f.write("Generated Subtitles:\n\n")
        f.write(text + "\n")

    os.remove(audio_path)
    return subtitle_txt_path
