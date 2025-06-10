from audio_player import AudioManager
from azure_tts_manager import AzureTTSManager

class TTSManager:

    audio_manager = AudioManager()
    azuretts_manager = AzureTTSManager()

    user_voice_name = "pt-BR-AntonioNeural"

    def __init__(self):
        file_path = self.azuretts_manager.text_to_audio("Ativado!") # Say something when the app starts
        self.audio_manager.play_audio(file_path, True, True)

    def update_voice_name(self, voice_name):
        self.user_voice_name = voice_name

    def text_to_audio(self, text, voice_name = "random"):
        tts_file = self.azuretts_manager.text_to_audio(text, voice_name)
        self.audio_manager.play_audio(tts_file, True, True)
