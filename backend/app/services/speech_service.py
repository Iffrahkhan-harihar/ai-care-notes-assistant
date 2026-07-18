# Converts audio files into text using Azure Speech-to-Text service
import azure.cognitiveservices.speech as speechsdk
from app.core.keyvault import get_secret

# Retrieve Azure Speech service credentials securely from Key Vault
speech_key = get_secret("speech-key")
speech_region = get_secret("speech-region")

# Transcribes audio file into text using Azure Speech SDK
def transcribe_audio(file_path: str) -> str:
    try:
        # Configure speech recognition with subscription credentials
        speech_config = speechsdk.SpeechConfig(
            subscription=speech_key,
            region=speech_region
        )

        # Load audio file from local path for transcription
        audio_config = speechsdk.audio.AudioConfig(filename=file_path)

        # Initialize speech recognizer with configuration
        recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config
        )

        # Perform one-time speech recognition on the audio file
        result = recognizer.recognize_once()

        # Return transcribed text if recognition is successful
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return result.text
        # Return empty string if transcription fails or no speech detected
        else:
            return ""

    # Handle transcription errors gracefully
    except Exception as e:
        print("❌ Transcription error:", e)
        return ""