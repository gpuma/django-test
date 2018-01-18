from celery import Celery
import time

app = Celery('tasks')
app.config_from_object('celeryconfig')

@app.task
def add(x, y):
    time.sleep(10)
    return x + y
