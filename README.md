# yapper-audio2audio-translation

Yapper is an audio to audio translation application that uses a pipeline of HuggingFace transformer models to translate user-recorded speech from English to Spanish and vice-versa. Here you will find instructions on how to run this application locally on your machine.

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
