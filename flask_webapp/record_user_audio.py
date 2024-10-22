import sounddevice as sd
import wave
import numpy as np
import tempfile
import threading

# Audio settings
FORMAT = 'float32'
CHANNELS = 1
RATE = 16000
CHUNK = 1024  # Process in small chunks to allow checking for input

# Global flag to signal when to stop recording
recording_flag = threading.Event()

def record_audio():
    print("Recording...")

    # List to store recorded chunks
    frames = []

    # Continuously record audio in chunks until the flag is cleared
    with sd.InputStream(samplerate=RATE, channels=CHANNELS, dtype=FORMAT, blocksize=CHUNK) as stream:
        while not recording_flag.is_set():
            data, _ = stream.read(CHUNK)
            frames.append(data)

    print("Recording stopped.")
    
    # Convert recorded frames to a numpy array
    audio_data = np.concatenate(frames)

    # Convert from float32 to int16 for WAV format
    audio_data = np.int16(audio_data * 32767)

    # Use a temporary file for saving the audio
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
        with wave.open(temp_audio_file.name, 'wb') as wave_file:
            wave_file.setnchannels(CHANNELS)
            wave_file.setsampwidth(2)  # 2 bytes for int16
            wave_file.setframerate(RATE)
            wave_file.writeframes(audio_data.tobytes())

        print(f"Recording saved to temporary file: '{temp_audio_file.name}'")

    # Return the temporary file path to use later
    return temp_audio_file.name
