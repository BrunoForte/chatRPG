class CurrentUser:
    def __init__(self, user_name, tts_enabled = True, voice_name = 'random', message = 'Conectado!'):
        self.user_name = user_name
        self.tts_enabled = tts_enabled
        self.voice_name = voice_name
        self.message = message

    def __repr__(self):
         return f"CurrentUser(user_name='{self.user_name}', tts_enabled={self.tts_enabled}, voice_name='{self.voice_name}', message='{self.message}')"
         
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
    
def createNewUser(user_name):
        return CurrentUser(user_name, message=f'{user_name} foi selecionado!')

def updateUser(user_instance, field_name, new_value):
    if hasattr(user_instance, field_name): # Verifica se o atributo existe na instância
        setattr(user_instance, field_name, new_value) # Define o valor do atributo
        print(f"Instância de '{user_instance.user_name}' atualizada: {field_name} = {new_value}")
    else:
        print(f"AVISO: Atributo '{field_name}' não encontrado na instância de CurrentUser.")
    return user_instance