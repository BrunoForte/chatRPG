from datetime import time
from audioplayer import AudioPlayer
import os
from mutagen.mp3 import MP3

class AudioManager:
    def play_audio(self, path, sleep = True, delete = True):

        print(f"Playing file with audioPlayer: {path}")
        audio = AudioPlayer(path)
        audio.play(block=True)

        if sleep:
            # Calculate length of the file, based on the file format
            _, ext = os.path.splitext(path)
            mp3_file = MP3(path)
            file_length = mp3_file.info.length
        
        else:
            print("Cannot play audio, unknown file type")
            return
        
        # Sleep until file is done playing
        time.sleep(file_length)

        #Delete the file after played
        if delete:
            audio.stop()
            try:
                os.remove(path)
                print(f'audio file deleted.')
            except PermissionError:
                print(f"Audio file {path} used by another process. Can't delete.")
