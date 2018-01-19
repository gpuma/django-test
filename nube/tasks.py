# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from time import sleep
from .word_cloud import WordCloud


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    # sleep(5)
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def create_word_cloud_task(content, type, save_folder):
    wc = WordCloud(content, type=type)
    filename = wc.save_word_cloud_to_fs(save_folder)
    return filename
