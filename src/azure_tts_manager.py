import azure.cognitiveservices.speech as speech

AZURE_VOICES =[
    "pt-BR-BrendaNeural",
    "pt-BR-FranciscaNeural",
    "pt-BR-AntonioNeural",
    "pt-BR-BrendaNeural",
    "pt-BR-DonatoNeural",
    "pt-BR-FabioNeural",
    "pt-BR-HumbertoNeural",
    "pt-BR-JulioNeural",
    "pt-BR-LeilaNeural",
    "pt-BR-ManuelaNeural",
    "pt-BR-ThalitaNeural",
    "pt-PT-RaquelNeural",
    "pt-PT-DuarteNeural",
    "pt-PT-FernandaNeural",
]

class AzureTTSManager:
    def __init__(self):
        print(f"test azure tts manager")