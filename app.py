from flask import Flask, render_template, request, jsonify
import os
import uuid
import speech_recognition as sr
from werkzeug.utils import secure_filename
from modules.speech_to_text import transcribe_audio
#from googletrans import Translator
from deep_translator import GoogleTranslator
from pydub import AudioSegment

from gtts import gTTS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')

jwt = JWTManager(app)

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if username == 'admin' and password == 'password':
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify({'msg': 'Bad username or password'}), 401

@app.route('/speech-to-text', methods=['GET', 'POST'])
def speech_to_text():
    transcription = None
    if request.method == 'POST':
        if 'audio_file' not in request.files:
            return render_template('speech_to_text.html', transcription='No file uploaded')
        file = request.files['audio_file']
        if file.filename == '':
            return render_template('speech_to_text.html', transcription='No file selected')
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            transcription = transcribe_audio(filepath)
            os.remove(filepath)
    return render_template('speech_to_text.html', transcription=transcription)

@app.route('/text-to-speech', methods=['GET', 'POST'])
def text_to_speech():
    audio_file = None
    if request.method == 'POST':
        try:
            text = request.form.get('text_input')
            print(f"Received text for TTS: {text}")
            if text:
                from modules.text_to_speech import text_to_speech as tts
                audio_file = tts(text)
                print(f"Generated audio file: {audio_file}")
                if audio_file.startswith('static/'):
                    audio_file = audio_file[len('static/'):]
        except Exception as e:
            audio_file = 'audio/output.mp3'
            print(f"Error in text_to_speech processing: {e}")
    return render_template('text_to_speech.html', audio_file=audio_file)

@app.route('/image-description', methods=['GET', 'POST'])
def image_description():
    description = None
    audio_file = None
    if request.method == 'POST':
        try:
            if 'image_file' not in request.files:
                return render_template('image_description.html', description='No file uploaded')
            file = request.files['image_file']
            print(f"Received image file: {file.filename}")
            if file.filename == '':
                return render_template('image_description.html', description='No file selected')
            if file:
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                print(f"Saved image file to: {filepath}")
                from modules.image_description import image_to_audio
                description, audio_file = image_to_audio(filepath)
                print(f"Generated description: {description}")
                print(f"Generated audio file: {audio_file}")
                audio_file = audio_file.replace('static/', '')
                os.remove(filepath)
        except Exception as e:
            description = None
            audio_file = None
            print(f"Error in image_description processing: {e}")
    return render_template('image_description.html', description=description, audio_file=audio_file)

@app.route('/video-subtitles', methods=['GET', 'POST'])
def video_subtitles():
    subtitle_file = None
    if request.method == 'POST':
        try:
            if 'video_file' not in request.files:
                return render_template('video_subtitles.html', subtitle_file=None)
            file = request.files['video_file']
            print(f"Received video file: {file.filename}")
            if file.filename == '':
                return render_template('video_subtitles.html', subtitle_file=None)
            if file:
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                print(f"Saved video file to: {filepath}")
                from modules.video_subtitles import generate_subtitles
                subtitle_path = generate_subtitles(filepath)
                print(f"Generated subtitle file: {subtitle_path}")
                subtitle_file = subtitle_path.replace('static/', '')
                os.remove(filepath)
        except Exception as e:
            subtitle_file = None
            print(f"Error in video_subtitles processing: {e}")
    return render_template('video_subtitles.html', subtitle_file=subtitle_file)

@app.route('/live-speech-to-text', methods=['GET', 'POST'])
def live_speech_to_text():
    if request.method == 'GET':
        return render_template('live_speech_to_text.html')
    elif request.method == 'POST':
        if 'audio_data' not in request.files:
            return jsonify({'error': 'No audio data uploaded'}), 400
        audio_file = request.files['audio_data']
        if audio_file.filename == '':
            return jsonify({'error': 'No audio file selected'}), 400

        filename_webm = secure_filename(f"{uuid.uuid4()}.webm")
        filepath_webm = os.path.join(app.config['UPLOAD_FOLDER'], filename_webm)
        audio_file.save(filepath_webm)

        filename_wav = f"{uuid.uuid4()}.wav"
        filepath_wav = os.path.join(app.config['UPLOAD_FOLDER'], filename_wav)
        
        audio = AudioSegment.from_file(filepath_webm, format="webm")
        audio.export(filepath_wav, format="wav")

        recognizer = sr.Recognizer()
        transcription = ""
        try:
            with sr.AudioFile(filepath_wav) as source:
                audio_data = recognizer.record(source)
            transcription = recognizer.recognize_google(audio_data)
        except Exception as e:
            transcription = f"Error recognizing speech: {e}"

        os.remove(filepath_webm)
        os.remove(filepath_wav)
        return jsonify({'transcription': transcription})

@app.route('/live-speech-translation', methods=['GET', 'POST'])
def live_speech_translation():
    if request.method == 'GET':
        return render_template('live_speech_translation.html')
    elif request.method == 'POST':
        if 'audio_data' not in request.files:
            return jsonify({'error': 'No audio data uploaded'}), 400
        audio_file = request.files['audio_data']
        language = request.form.get('language')

        if audio_file.filename == '':
            return jsonify({'error': 'No audio file selected'}), 400

        filename_webm = secure_filename(f"{uuid.uuid4()}.webm")
        filepath_webm = os.path.join(app.config['UPLOAD_FOLDER'], filename_webm)
        audio_file.save(filepath_webm)

        filename_wav = f"{uuid.uuid4()}.wav"
        filepath_wav = os.path.join(app.config['UPLOAD_FOLDER'], filename_wav)
        sound = AudioSegment.from_file(filepath_webm, format="webm")
        sound.export(filepath_wav, format="wav")

        recognizer = sr.Recognizer()
        transcription = ""
        translation = ""
        translated_audio_file = None
        try:
            with sr.AudioFile(filepath_wav) as source:
                audio_data = recognizer.record(source)
            transcription = recognizer.recognize_google(audio_data)

            # if transcription:
            #     translator = Translator()
            #     translated_text = translator.translate(transcription, dest=language).text
            #     translation = translated_text
            if transcription:
                translation = GoogleTranslator(source='auto', target=language).translate(transcription)
            
                tts = gTTS(text=translation, lang=language)
                translated_audio_filename = f"static/audio/{uuid.uuid4()}.mp3"
                tts.save(translated_audio_filename)
                translated_audio_file = '/' + translated_audio_filename
        except Exception as e:
            transcription = f"Error recognizing speech: {e}"
            print(e) # For debugging

        os.remove(filepath_webm)
        os.remove(filepath_wav)
        return jsonify({'transcription': transcription, 'translation': translation, 'audio_file': translated_audio_file})

if __name__ == '__main__':
    app.run(debug=True)