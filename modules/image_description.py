from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
from PIL import Image
from gtts import gTTS
import os

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def image_to_audio(image_path):
    image = Image.open(image_path).convert('RGB')
    inputs = processor(image, return_tensors="pt")

    out = model.generate(**inputs)
    description = processor.decode(out[0], skip_special_tokens=True)

    # Convert description to audio using gTTS
    audio_file = "static/audio/image_description.mp3"
    tts = gTTS(text=description, lang='en')
    try:
        if not os.path.exists('static/audio'):
            os.makedirs('static/audio')
        tts.save(audio_file)
    except Exception as e:
        print(f"Error saving audio file: {e}")
        audio_file = None

    return description, audio_file
