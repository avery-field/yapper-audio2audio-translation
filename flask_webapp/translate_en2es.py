from transformers import pipeline
import soundfile as sf
from datasets import load_dataset


# ASR English
audio2text = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-base.en",
    chunk_length_s=30,
) 

# Translator EN to ES
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-es", device='cpu')

# Spanish text to speech
text2audio = pipeline(model="ylacombe/mms-spa-finetuned-chilean-monospeaker")

def translate(input_path, output_path):
    # Load audio data from file
    audio_data, samplerate = sf.read(input_path)
    
    # Prepare audio data for ASR model
    audio_dict = {
        "array": audio_data,
        "sampling_rate": samplerate
    }
    english_text = audio2text(audio_data, batch_size=8)
    print(english_text)
    spanish_text = translator(english_text['text'])
    spanish_text = spanish_text[0]['translation_text']
    print(spanish_text)
    speech = text2audio(spanish_text)
    
    sf.write(output_path, speech["audio"].squeeze(), speech["sampling_rate"])

    return spanish_text

if __name__ == "__main__":
    print('\nTRANSLATING AUDIO...\n')
    audio_input = '/path/to/audio_input.wav'
    output_path = '/path/to/translated_audio.wav'
    translate(audio_input, output_path)