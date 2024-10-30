# yapper-audio2audio-translation

Yapper is an audio to audio translation application that uses a pipeline of HuggingFace transformer models to translate user-recorded speech from English to Spanish and vice-versa. 

## Installation
Clone this repository and navigate to the project directory:


```
git clone https://github.com/<username>/<project-name>.git
cd <project-name>
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
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```
Navigate to http://localhost:5000/ in your web browser to access the app.
