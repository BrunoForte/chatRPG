class CurrentUser:
    def __init__(self, user_name, tts_enabled = True, voice_name = 'random', message = 'Conectado!'):
        self.user_name = user_name
        self.tts_enabled = tts_enabled
        self.voice_name = voice_name
        self.message = message

    def serialize(self, old_id = None):
        if old_id is not None:
            return {'user': self.user_name, 
                    'tts': self.tts_enabled,
                    'message': self.message, 
                    'voice': self.voice_name, 
                    'old_id': old_id}
        else:
            return {'user': self.user_name, 
                    'tts': self.tts_enabled,
                    'message': self.message, 
                    'voice': self.voice_name }
    
def createNewUser(user):
        return CurrentUser(user, message=f'{user} foi selecionado!')

def updateUser(user, field, value):
    user = CurrentUser(user, field = value)
    return user