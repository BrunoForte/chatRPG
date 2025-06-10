import os
import random
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
    azure_speechconfig = None
    azure_synthesizer = None

    def __init__(self):
        self.azure_speechconfig = speech.SpeechConfig(subscription= os.getenv('AZURE_TTS_KEY'), region = 'brazilsouth')
        self.azure_speechconfig.speech_synthesis_voice_name = "pt-BR-BrendaNeural"
        self.azure_synthesizer = speech.SpeechSynthesizer(speech_config = self.azure_speechconfig, audio_config = None)

    #Returns the path to the new .wav file

    def text_to_audio(self, text: str, voice_name = "random"):
        voice_name = (random.choice(AZURE_VOICES) if voice_name == "random" else voice_name)
        ssml_text = f"<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' xmlns:emo='http://www.w3.org/2009/10/emotionml' xml:lang='en-US'><voice name='{voice_name}'>{text}</voice></speak>"
        result = self.azure_synthesizer.speak_ssml_async(ssml_text).get()
        output = os.path.join(os.path.abspath(os.curdir + f"\\audios"), f"_Msg{str(hash(text))}{str(hash(voice_name))}.wav")
        
        if result.reason == speech.ResultReason.SynthesizingAudioCompleted:
            stream = speech.AudioDataStream(result)
            stream.save_to_wav_file(output)
        else:
            # if azure fails
            print("\n Azure failed. \n")
        return output
