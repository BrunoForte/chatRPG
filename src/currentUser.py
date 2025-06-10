class CurrentUser:
    def __init__(self, tts_enabled = True, voice_name = 'random', message = None):
        self.tts_enabled = tts_enabled
        self.voice_name = voice_name
        self.message = message

