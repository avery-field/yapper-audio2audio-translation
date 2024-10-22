from transformers import pipeline
import soundfile as sf
from datasets import load_dataset
from gtts import gTTS
from pydub import AudioSegment

#ASR SPANISH
audio2text = pipeline(model="openai/whisper-tiny", 
                      task="automatic-speech-recognition")

# Translator ES to EN
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-es-en", device='cpu')

def text2audio(text):
    tts = gTTS(text=text, lang='en')
    return tts

def translate(input_path, output_path):
    # Load audio data from file
    audio_data, samplerate = sf.read(input_path)
    
    # Prepare audio data for ASR model
    audio_dict = {
        "array": audio_data,
        "sampling_rate": samplerate
    }
    spanish_text = audio2text(audio_data, batch_size=8)
    print(spanish_text['text'])
    english_text = translator(spanish_text['text'])
    english_text = english_text[0]['translation_text']
    print(english_text)
    spanish_speech = text2audio(english_text)
    spanish_speech.save(output_path + ".mp3")
    
    # Convert mp3 to wav using pydub
    sound = AudioSegment.from_mp3(output_path + ".mp3")
    sound.export(output_path, format="wav")

    return english_text

if __name__ == "__main__":
    print('\nTRANSLATING AUDIO...\n')
    audio_input = '/path/to/audio_input.wav'
    output_path = '/path/to/translated_audio.wav'
    translate(audio_input, output_path)