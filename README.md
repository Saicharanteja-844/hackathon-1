# hackathon-1
## AI-Powered Accessibility Tool
Develop AI tools for people with disabilities:
- Speech-to-text & text-to-speech for hearing/speech impaired
- Image-to-audio descriptions for visually impaired
- Real-time subtitle generator for videos

## Libraries and APIs Used

Below is a comprehensive list of all libraries and APIs used in the project, based on the `requirements.txt` file and code analysis. I've explained the purpose of each and why they were chosen.

### Core Web Framework
- **Flask**: A lightweight web framework for Python. Used to build the web application, handle routing, and serve templates. Chosen for its simplicity, flexibility, and minimal overhead compared to heavier frameworks like Django, making it ideal for a multi-feature app with various modules.

### Speech Recognition and Processing
- **speechrecognition**: Library for performing speech recognition. Used in `modules/speech_to_text.py` for converting audio files or live speech to text. It supports multiple engines, including Google's Speech API, which provides high accuracy for transcription tasks.
- **gTTS (Google Text-to-Speech)**: Converts text to speech using Google's TTS service. Used in `modules/text_to_speech.py` to generate audio from text input. Selected for its free, high-quality voice synthesis and ease of integration.
- **pydub**: Audio processing library. Used for manipulating audio files (e.g., converting formats, trimming). Essential for preprocessing audio before speech recognition or after TTS generation.

### Image and Video Processing
- **Pillow (PIL)**: Python Imaging Library for image processing. Used in `modules/image_description.py` for opening and handling image files. Chosen for its comprehensive image manipulation capabilities and wide support.
- **moviepy**: Video editing library. Used in `modules/video_subtitles.py` for processing video files, extracting audio, and adding subtitles. Relies on FFmpeg for backend processing; selected for its Pythonic API and ability to handle complex video operations.
- **transformers**: Hugging Face library for natural language processing and computer vision models. Used for image description tasks (e.g., generating captions from images using models like BLIP). Provides state-of-the-art pre-trained models for accurate AI-powered descriptions.
- **torch**: PyTorch deep learning framework. Dependency for `transformers` and other ML models. Used for running neural networks efficiently on CPU/GPU.

### Translation and Language Services
- **deep-translator**: Library for text translation using various APIs. Used for translating text between languages. Chosen over direct API calls for its unified interface to multiple translation services (e.g., Google Translate), making it easy to switch providers if needed.

### External APIs Integrated
- **Google Speech Recognition API**: Accessed via `speechrecognition` library. Used for accurate speech-to-text conversion. Chosen for its reliability and no-cost tier for development.
- **Google Text-to-Speech API**: Accessed via `gTTS`. Provides natural-sounding voice synthesis. Selected for its free access and high-quality output.
- **Google Translate API**: Accessed via `deep-translator`. Used for language translation features. Chosen for its extensive language support and accuracy.
- **Hugging Face Models (via transformers)**: Pre-trained AI models for image captioning. Used for generating descriptive text from images. Selected for their open-source nature, ease of use, and strong performance in computer vision tasks.

### Additional Notes
- The project also uses standard Python libraries implicitly (e.g., `os`, `json`, `pickle` for model loading in `model.py`), but they are not listed in `requirements.txt` as they are part of Python's standard library.
- For the loan prediction feature, the code uses `pickle` to load a pre-trained model (`loan_model.pkl`), but dependencies like `scikit-learn`, `pandas`, and `numpy` are not in `requirements.txt`. If the model requires them, they should be added to ensure the app runs without errors.
- FFmpeg is required for video processing (via `moviepy`) but is not a Python package; it's a separate system tool, as noted in `FFmpeg_Installation_Instructions.txt`.

This setup provides a robust, multi-modal application for speech, image, video, and text processing, with secure authentication and translation capabilities.
