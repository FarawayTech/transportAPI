"""Synthesizes speech from the input string of text or ssml.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
import os
import json

from google.oauth2 import service_account

from . import BaseTTSApi
from google.cloud import texttospeech

# Read env data
credentials_raw = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

# Generate credentials
service_account_info = json.loads(credentials_raw)
credentials = service_account.Credentials.from_service_account_info(
    service_account_info)

# Define a client, in this case Google's text to speech
client = texttospeech.TextToSpeechClient(credentials=credentials)


class GoogleTTSApi(BaseTTSApi):

    def get_voice_mp3(self, text: str) -> texttospeech.types.SynthesizeSpeechResponse:

        # Set the text input to be synthesized
        synthesis_input = texttospeech.types.SynthesisInput(text=text)

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        voice = texttospeech.types.VoiceSelectionParams(
            language_code='en-US',
            ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE,
            name="en-US-Wavenet-F"
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3,
            speaking_rate=1.1)

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(synthesis_input, voice, audio_config)

        return response
