# Phuyu
Phuyu, which means cloud in Quechua, is a small web application for word cloud generation, inspired by Wordie.
Phuyu uses its own greedy algorithm for cloud generation, based on word frequency.

## What's a word cloud?
A word cloud is a visualization of the words on a text. The most frequent words are emphasized. Word clouds
can be used for NLP purposes, data analysis or just for fun :). Here's an example output from Phuyu:

![alt text](example.png)

## Demo
`coming soon`

## Main Technologies
- Django 2.0 is used as the framework
- NLTK is used to determine stopwords
- Pillow is used for image generation
- Celery is used for asynchronous task processing
- RabbitMQ is used as a message broker

## Building the project
- clone the repo: `git clone http://github.com/gpuma/phuyu`
- create a virtualenv. For example: `python3 -m venv venv`
- activate the virtual env:
  - Windows: `venv\Scripts\activate.bat`
  - Linux: `source venv/bin/activate`
- install dependencies: `pip install -r requirements.txt`
- create Django models: `python manage.py migrate`
- install RabbitMQ server. Check below for details
- download NLTK corpus; enter the following in a python shell:
  - `import nltk`
  - `nltk.download('stopwords')`
- check `nube/constants.py` and make sure `FONT_LOCATION` is set to an existing font in your filesystem
- deploy the django server: `python manage.py runserver`
- deploy the worker server: `celery -A phuyu worker -l info`
- go to http://localhost:8000/nube/ (default port)

## Limitations
- Phuyu supports only english text for now

## Some info
- Images are stored in `media` folder
- If you're interested only in the algorithm, check `word_cloud.py`.

## Installing RabbitMQ
- Linux: `sudo apt-get install rabbitmq-server`
- Windows: follow this guide: http://www.rabbitmq.com/download.html
  - IMPORTANT: You also need to define the following environment variable:
  `FORKED_BY_MULTIPROCESSING=1`
