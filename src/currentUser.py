from userType import UserType

class CurrentUser:
    def __init__(self, user_name, tts_enabled = True, voice_name = 'random', message = 'Conectado!', user_type = UserType.NULL):
        self.user_name = user_name
        self.tts_enabled = tts_enabled
        self.voice_name = voice_name
        self.message = message
        self.user_type = user_type

    def serialize(self):
        return {
            'user': self.user_name,
            'tts': self.tts_enabled,
            'message': self.message,
            'voice': self.voice_name
        }
    
def createNewUser(user):
    return CurrentUser(user, message=f'{user} foi selecionado!', user_type=UserType.NEW)

def updateUser(user, field, value):
    user = CurrentUser(user, field = value)
    return user