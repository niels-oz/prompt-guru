# Prompt Guru

This is a Python application that allows you to craft your Chat GPT prompt.

## Status

save session and load session not yet implemented.

## How it works

The application provides you with a playground to query Chat GPT. It records all your prompts and settings. And allows
you to download and rerun them. The application uses Streamlit to create the GUI to create the prompt. It uses 
ChatGPT's complete webservice to query the LLM.


## Installation

To install the repository, please clone this repository, create a virtual environment and install the requirements:

```
git clone https://github.com/niels-oz/prompt-guru.git
cd prompt-guru
python3 -m venv ../venv/prompt-guru
source ../venv/prompt-guru/bin/activate
pip install -r requirements.txt
```

To create an openAI API key goto https://platform.openai.com/account/api-keys. 

Create a `.env` file from the .env.example. And add your OpenAI API key to it.

## Usage

To use the application, run the `app.py` file: 

```
streamlit run app.py
```

