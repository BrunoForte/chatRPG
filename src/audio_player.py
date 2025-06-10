import os
import time
import soundfile as sf
from audioplayer import AudioPlayer
from mutagen.mp3 import MP3

class AudioManager:
    def play_audio(self, path, sleep = True, delete = True):

        print(f"Playing file with audioPlayer: {path}")
        audio = AudioPlayer(path)
        audio.play(block=True)

        if sleep:
            # Calculate length of the file, based on the file format
            _, ext = os.path.splitext(path)
            if ext.lower() == '.wav':
                file_length = sf.SoundFile(path).frames / sf.SoundFile(path).samplerate
            elif ext.lower() == '.mp3':
                file_length = MP3(path).info.length
            else:
                print(f"Cannot play audio, unknown file type")
                return
                
        # Sleep until file is done playing
        time.sleep(file_length)
        audio.close()

        #Delete the file after played
        if delete:
            try:
                os.remove(path)
                print(f'audio file deleted.')
            except OSError as e:
                print(f"Erro ao remover arquivo: {e}")
