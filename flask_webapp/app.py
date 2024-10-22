import os
import csv
import time
from flask import Flask, render_template, request, jsonify, send_file
import threading
from record_user_audio import record_audio, recording_flag
from translate_en2es import translate
from translate_es2en import translate as translate_es2en

app = Flask(__name__)

# Define the static directory
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

# Time threshold for deleting old files (in seconds)
TIME_THRESHOLD = 300  # 5 minutes

# Global variable to store audio file paths
audio_file = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_recording', methods=['POST'])
def start_recording():
    global audio_file
    recording_flag.clear()  # Reset the recording flag
    threading.Thread(target=record_audio_thread).start()
    return jsonify({"message": "Recording started"}), 200

@app.route('/stop_recording', methods=['POST'])
def stop_recording():
    global audio_file
    recording_flag.set()  # Signal the recording thread to stop
    time.sleep(1)  # Wait for the thread to finish
    if audio_file:
        return jsonify({"message": "Recording stopped", "audio_file": audio_file}), 200
    else:
        return jsonify({"message": "No audio recorded"}), 400

def record_audio_thread():
    global audio_file
    audio_file = record_audio()

@app.route('/translate_audio', methods=['POST'])
def translate_audio():
    global audio_file
    data = request.get_json()
    target_lang = data.get('target_lang')

    if not audio_file:
        return jsonify({"message": "No audio to translate"}), 400

    # Generate a unique filename for the translated output using timestamp
    timestamp = str(int(time.time()))
    translated_filename = f"translated_audio_{timestamp}.wav"
    translated_audio_file = os.path.join(STATIC_DIR, translated_filename)

    # Call the appropriate translate function based on target language
    if target_lang == 'es':
        translated_text = translate(audio_file, translated_audio_file)
    elif target_lang == 'en':
        translated_text = translate_es2en(audio_file, translated_audio_file)
    else:
        return jsonify({"message": "Invalid target language"}), 400

    return jsonify({
        "message": "Audio translated successfully",
        "translated_file": f"/static/{translated_filename}",  # Return the unique URL
        "translated_text": translated_text  # Send the translated text back
    }), 200

@app.route('/play_translation', methods=['POST'])
def play_translation():
    data = request.get_json()
    translated_file_url = data.get('translated_file')

    if translated_file_url:
        return jsonify({
            "message": "Playing translated audio",
            "audio_url": translated_file_url  # Return the correct URL to the frontend
        })
    else:
        return jsonify({"message": "No translated audio available"}), 400

@app.route('/bad_translation', methods=['POST'])
def bad_translation():
    data = request.get_json()
    bad_translation = data.get('bad_translation')
    target_lang = data.get('target_lang')

    # Check for missing data
    if not bad_translation or not target_lang:
        return jsonify({"message": "Bad translation or target language missing"}), 400
    
    # Path for the CSV file
    csv_file = 'bad_translations.csv'

    # Check if the file exists to know if headers should be written
    file_exists = os.path.isfile(csv_file)

    try:
        # Open the CSV file in append mode
        with open(csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['target_lang', 'bad_translation'])

            # Write header if the file is new
            if not file_exists:
                writer.writeheader()

            # Write the bad translation as a new row
            writer.writerow({
                'target_lang': target_lang,
                'bad_translation': bad_translation
            })

        return jsonify({"message": "Bad translation saved to CSV successfully!"}), 200
    except Exception as e:
        return jsonify({"message": f"Failed to save bad translation: {str(e)}"}), 500


def cleanup_old_files():
    """Periodically cleans up old translation files from the static directory."""
    while True:
        current_time = time.time()

        # Iterate over all files in the static directory
        for filename in os.listdir(STATIC_DIR):
            file_path = os.path.join(STATIC_DIR, filename)

            # Check if the file is old enough to be deleted
            if os.path.isfile(file_path):
                file_age = current_time - os.path.getmtime(file_path)
                if file_age > TIME_THRESHOLD:
                    print(f"Deleting old file: {file_path}")
                    os.remove(file_path)

        # Sleep for a while before checking again
        time.sleep(60)  # Run the cleanup task every minute

if __name__ == "__main__":
    # Start the cleanup thread in the background
    cleanup_thread = threading.Thread(target=cleanup_old_files)
    cleanup_thread.daemon = True  # Ensure the thread will exit when the main program exits
    cleanup_thread.start()

    # Start the Flask app
    app.run(debug=True)



