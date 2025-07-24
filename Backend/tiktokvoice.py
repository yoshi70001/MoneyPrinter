# Modified to use edge-tts instead of TikTok TTS

import asyncio
import edge_tts

from typing import List
from termcolor import colored
from playsound import playsound


# Common voices used in the application
VOICES = [
    # English Voices
    "en-US-JennyNeural",      # Female
    "en-US-GuyNeural",        # Male
    "en-GB-SoniaNeural",      # British Female
    "en-GB-RyanNeural",       # British Male
    "en-AU-NatashaNeural",    # Australian Female
    "en-AU-WilliamNeural",    # Australian Male
    # European Voices
    "fr-FR-DeniseNeural",     # French Female
    "fr-FR-HenriNeural",      # French Male
    "de-DE-KatjaNeural",      # German Female
    "de-DE-ConradNeural",     # German Male
    "es-ES-ElviraNeural",     # Spanish Female
    "es-ES-AlvaroNeural",     # Spanish Male
    # American Voices
    "es-MX-DaliaNeural",      # Mexican Spanish Female
    "es-MX-JorgeNeural",      # Mexican Spanish Male
    "pt-BR-FranciscaNeural",  # Brazilian Portuguese Female
    "pt-BR-AntonioNeural",    # Brazilian Portuguese Male
    "es-AR-ElenaNeural",      # Argentine Spanish Female
    # Asian Voices
    "ja-JP-NanamiNeural",     # Japanese Female
    "ja-JP-KeitaNeural",      # Japanese Male
    "ko-KR-SunHiNeural",      # Korean Female
    "ko-KR-InJoonNeural",     # Korean Male
]

# Maximum text length for a single conversion (edge-tts has a much higher limit than TikTok TTS)
TEXT_BYTE_LIMIT = 3000


# create a list by splitting a string, every element has n chars
def split_string(string: str, chunk_size: int) -> List[str]:
    words = string.split()
    result = []
    current_chunk = ""
    for word in words:
        if (
            len(current_chunk) + len(word) + 1 <= chunk_size
        ):  # Check if adding the word exceeds the chunk size
            current_chunk += f" {word}"
        else:
            if current_chunk:  # Append the current chunk if not empty
                result.append(current_chunk.strip())
            current_chunk = word
    if current_chunk:  # Append the last chunk if not empty
        result.append(current_chunk.strip())
    return result


# Generate audio using edge-tts
async def generate_audio(text: str, voice: str) -> None:
    communicate = edge_tts.Communicate(text, voice)
    return communicate


# creates a text to speech audio file
def tts(
    text: str,
    voice: str = "none",
    filename: str = "output.mp3",
    play_sound: bool = False,
) -> None:
    # checking if arguments are valid
    if voice == "none":
        print(colored("[-] Please specify a voice", "red"))
        return

    if voice not in VOICES:
        print(colored("[-] Voice not available", "red"))
        return

    if not text:
        print(colored("[-] Please specify a text", "red"))
        return

    # creating the audio file
    try:
        if len(text) < TEXT_BYTE_LIMIT:
            # Create event loop if it doesn't exist
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            # Generate and save audio
            async def process_audio():
                communicate = await generate_audio(text, voice)
                await communicate.save(filename)

            loop.run_until_complete(process_audio())
        else:
            # Split longer text into smaller parts
            text_parts = split_string(text, TEXT_BYTE_LIMIT - 1)
            temp_files = []

            # Generate audio for each part
            async def process_parts():
                for i, text_part in enumerate(text_parts):
                    temp_file = f"temp_{i}.mp3"
                    communicate = await generate_audio(text_part, voice)
                    await communicate.save(temp_file)
                    temp_files.append(temp_file)

            # Create event loop if it doesn't exist
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            loop.run_until_complete(process_parts())

            # Concatenate audio files
            import subprocess
            concat_list = "concat:" + "|".join(temp_files)
            subprocess.run(["ffmpeg", "-i", concat_list, "-acodec", "copy", filename])

            # Clean up temp files
            for temp_file in temp_files:
                import os
                os.remove(temp_file)

        print(colored(f"[+] Audio file saved successfully as '{filename}'", "green"))
        if play_sound:
            playsound(filename)

    except Exception as e:
        print(colored(f"[-] An error occurred during TTS: {e}", "red"))
