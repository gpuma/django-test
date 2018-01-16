from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from .word_cloud import WordCloud
from requests.exceptions import MissingSchema

from .constants import *

#class IndexView(generic.FormView):
    #template_name = 'nube/index.html'

def index(request):
    # todo: turn this into a generic view?
    return render(request, 'nube/index.html')

def create(request):
    """
    Displays the generated WordCloud from the
    given URI
    """
    response = HttpResponse(content_type="image/png")
    if request.POST['uri'] == '':
        return render(request, 'nube/index.html', {
            'error_message': URI_NOT_SPECIFIED
        })
    try:
        cloud = WordCloud(request.POST['uri'], type="internet")
    except (MissingSchema):
        # todo: this might need a redirect instead
        return render(request, 'nube/index.html', {
            'error_message': URI_COULD_NOT_BE_PROCESSED
        })
    else:
        img = cloud.get_word_cloud_as_image()
        img.save(response, 'PNG')
        return response
