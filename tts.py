from elevenlabs import set_api_key, generate, voices, save
import os


class TTS:
    def __init__(self, env):
        self.env = env
        set_api_key(env['ELEVENLABS_API_KEY'])
        self.voices = voices()
        self.Paola = self.findVoice(self.voices, "Paola")
        self.Adam = self.findVoice(self.voices, "Adam")

    def findVoice(self, voices, name):
        for voice in voices:
            if voice.name == name:
                return voice
        return None

    def createAudio(self, text, gender, language="english"):
        print("Creating audio file")
        if self.env['DEBUG'].upper() == 'TRUE':
            print("DEBUG: Using test audio file")
            return os.path.join('test_files', 'tts-audio-files', 'english.mp3')
        voice = self.Paola
        if gender == "M":
            voice = self.Adam
        if language == "english":
            audio = generate(
                text, voice=voice, model="eleven_monolingual_v1")
            fileName = os.path.join('tts-audio-files', 'english.mp3')
        else:
            audio = generate(
                text, voice=voice, model="eleven_multilingual_v1")
            fileName = os.path.join('tts-audio-files', language+'.mp3')
        save(audio, fileName)
        return fileName
