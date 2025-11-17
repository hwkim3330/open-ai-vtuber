import sys
import os
import re

import edge_tts
from loguru import logger
from .tts_interface import TTSInterface

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)


# Check out doc at https://github.com/rany2/edge-tts
# Use `edge-tts --list-voices` to list all available voices


class TTSEngine(TTSInterface):
    def __init__(self, voice="en-US-AvaMultilingualNeural"):
        self.voice = voice

        self.temp_audio_file = "temp"
        self.file_extension = "mp3"
        self.new_audio_dir = "cache"

        if not os.path.exists(self.new_audio_dir):
            os.makedirs(self.new_audio_dir)

    def convert_markdown_to_ssml(self, text):
        """
        Convert **text** markdown to SSML prosody tags for higher pitch.
        **text** → <prosody pitch="+30%">text</prosody>
        """
        # Convert **text** to higher pitch SSML
        text = re.sub(r'\*\*(.+?)\*\*', r'<prosody pitch="+30%">\1</prosody>', text)

        # Wrap in speak tag if SSML tags are present
        if '<prosody' in text:
            text = f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">{text}</speak>'

        return text

    def generate_audio(self, text, file_name_no_ext=None):
        """
        Generate speech audio file using TTS.
        text: str
            the text to speak
        file_name_no_ext: str
            name of the file without extension


        Returns:
        str: the path to the generated audio file

        """
        file_name = self.generate_cache_file_name(file_name_no_ext, self.file_extension)

        # Convert **text** to SSML for pitch control
        text_with_ssml = self.convert_markdown_to_ssml(text)

        try:
            communicate = edge_tts.Communicate(text_with_ssml, self.voice)
            communicate.save_sync(file_name)
        except Exception as e:
            logger.critical(f"\nError: edge-tts unable to generate audio: {e}")
            logger.critical("It's possible that edge-tts is blocked in your region.")
            return None

        return file_name


# en-US-AvaMultilingualNeural
# en-US-EmmaMultilingualNeural
# en-US-JennyNeural
