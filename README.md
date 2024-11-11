# yapper-audio2audio-translation

Yapper is an audio to audio translation application that uses a pipeline of HuggingFace transformer models to translate user-recorded speech from English to Spanish and vice-versa. 
This system consists of three main components, a script that allows users to record their own speech and then preprocess their speech to be translated. The next component is an audio to audio translation pipeline. The final main component is the web app built using the Flask framework which hosts everything in one easy to interact with, user interface. The input of the system is the user recorded speech as an audio file and the output is the translated audio and text. Input data is stored as a temporary file which can be accessed by the translation pipeline script. Output is stored in the static directory of the web app.

Structure diagram for the web app:

flask-webapp/ 
├── app.py 
├── record_user_audio.py
├── translate_en2es.py 
├── translate_es2en.py 
├── templates/ 
    └── index.html 
└── static/ 
    └── translated_audio.wav

The audio to audio translation pipeline consists of three steps, each performed by a model accessed from HuggingFace. The first task is converting user recorded speech into text which was done using OpenAI's Whisper Automatic Speech Recognition model. The second task is taking that text and translating it from either English to Spanish or vice-verse using the Opus Machine Translation model developed at the University of Helsinki. The third task is converting that translated text back into audio using a Text to Speech model. For Spanish output, one of Meta's Massively Multilingual Speech model's finetuned on Chilean Spanish was used. For English output, Google's Text to Speech model was used.

Below, you will find instructions on how to run this application locally on your machine.

## Video Demo
https://drive.google.com/file/d/1VkkDdqtdO2wuYlYQBO916PKOjqDguBH1/view?usp=sharing

## Installation
Clone this repository and navigate to the project directory:


```
git clone https://github.com/avery-field/yapper-audio2audio-translation.git
cd yapper-audio2audio-translation
```

Create a virtual environment and install the required packages:


```
python -m venv venv
source venv/bin/activate  # on Windows, use "venv\Scripts\activate"
pip install -r requirements.txt
```


## Usage
Run the app locally using Flask:

```
python flask_webapp/app.py
```
Navigate to http://localhost:5000/ in your web browser to access the app.
