from elevenlabs.client import ElevenLabs
from elevenlabs import play, Voice, VoiceSettings
import os

TTSapi_key = None
client = ElevenLabs(api_key=TTSapi_key)


def generateTTS(message) -> None:
    file_path = './resources/TTS/audio_file.wav'
    audio = client.generate(text=message,
                            voice=Voice(voice_id="wcS3bcRLq413ziH06KeI",
                                        settings=VoiceSettings(speed=0.5,
                                                               stability=0.32,
                                                               similarity_boost=0.5
                                                               )))
    if os.path.isfile(file_path):
        os.remove(file_path)

    # drop audio file in resources/TTS folder
    with open('./resources/TTS/audio_file.wav', 'wb') as f:
        for chunk in audio:
            f.write(chunk)
