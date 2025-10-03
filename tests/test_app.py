import io
import os
import sys
import pytest

os.environ['JWT_SECRET'] = 'test_jwt_secret'

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_index(client):
    rv = client.get('/')
    assert rv.status_code == 200

def test_login(client):
    rv = client.post('/login', json={'username': 'admin', 'password': 'password'})
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert 'access_token' in json_data

def test_speech_to_text(client):
    data = {
        'audio_file': (io.BytesIO(b"fake audio data"), 'test.wav')
    }
    rv = client.post('/speech-to-text', data=data, content_type='multipart/form-data')
    assert rv.status_code == 200

def test_text_to_speech(client):
    data = {
        'text_input': 'Hello world'
    }
    rv = client.post('/text-to-speech', data=data)
    assert rv.status_code == 200

def test_image_description(client):
    data = {
        'image_file': (io.BytesIO(b"fake image data"), 'test.jpg')
    }
    rv = client.post('/image-description', data=data, content_type='multipart/form-data')
    assert rv.status_code == 200

def test_video_subtitles(client):
    data = {
        'video_file': (io.BytesIO(b"fake video data"), 'test.mp4')
    }
    rv = client.post('/video-subtitles', data=data, content_type='multipart/form-data')
    assert rv.status_code == 200

def test_live_speech_to_text(client):
    rv = client.get('/live-speech-to-text')
    assert rv.status_code == 200
