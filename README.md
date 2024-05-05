# INTRO

This is an example of a ollama model chat running on gradio. With this application, one can:

1. install ollama
2. run an ollama model (note: see https://ollama.com/library)
3. Specify the installed model in the main.py gr.Dropdown list.
4. Run the python application
5. The user chooses which model to run and submit a prompt.

# SETUP

## INSTALL OLLAMA:

### Download

https://ollama.com/download

### OLLAMA create models:

- ollama run tinyllama

### OLLAMA create Superman assistant:

- ollama create superman -f ./modelfile.txt

- ollama run superman

### List models:

- ollama list

## INSTALL gradio:

- pip install requests

- pip install json

- pip install gradio

- pip install time

- pip install GPUtil

- pip install psutil

# RUN

## RUN environment:

- python -m venv gradio-env

- source gradio-env/bin/activate

## RUN:

- python main.py

## Web link:

- http://127.0.0.1:7860

# REF:

https://github.com/jmorganca/ollama/tree/main/docs

https://www.gradio.app/guides/quickstart

https://www.gradio.app/guides/creating-a-chatbot-fast

https://github.com/jmorganca/ollama/blob/main/docs/import.md
