# django-test
placeholder

## building the project
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


## some info
- Images are stored in `media` folder

## installing RabbitMQ
- IMPORTANT: If you're on windows you need to define the following environment variable:
  `FORKED_BY_MULTIPROCESSING=1`
