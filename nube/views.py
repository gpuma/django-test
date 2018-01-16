from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from .word_cloud import WordCloud

#class IndexView(generic.FormView):
    #template_name = 'nube/index.html'

def index(request):
    # todo: turn this into a generic view?
    return render(request, 'nube/index.html',
                  {'header':'Welcome to Phuyu', 'subheader':'Select a plaintext'})

def create(request):
    """
    Displays the generated WordCloud from the
    given URI
    """
    response = HttpResponse(content_type="image/png")
    cloud = WordCloud(request.POST['uri'], type="internet")
    img = cloud.get_word_cloud_as_image()
    img.save(response, 'PNG')
    return response
