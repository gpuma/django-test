from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from .word_cloud import WordCloud

from .models import CloudImage

from requests.exceptions import MissingSchema

import os

# to generate a random filename
import uuid

from .constants import *

#class IndexView(generic.FormView):
    #template_name = 'nube/index.html'

def index(request):
    # todo: turn this into a generic view?
    return render(request, 'nube/index.html')

def create(request):
    """
    Displays the generated WordCloud from the
    given URI or uploaded file
    """
    response = HttpResponse(content_type="image/png")
    # in order to avoid KeyError
    myfile = request.FILES.get('myfile', None)

    if request.POST['uri'] == '' and myfile is None:
        return render(request, 'nube/index.html', {
            'error_message': NOTHING_TO_PROCESS
        })
    try:
        if myfile:
            cloud = WordCloud(myfile, type="upload")
        else:
            cloud = WordCloud(request.POST['uri'], type="internet")
    except (MissingSchema):
        # todo: this might need a redirect instead
        return render(request, 'nube/index.html', {
            'error_message': URI_COULD_NOT_BE_PROCESSED
        })
    else:
        img = cloud.get_word_cloud_as_image()
        filename = get_random_filename('.png')
        local_path = os.path.join(settings.MEDIA_ROOT, filename)
        img.save(local_path)
        return render(request, 'nube/cloud_image.html', {
            'img_filename': filename,
        })

class ImageDetailView(generic.DetailView):
    model = CloudImage
    template_name = 'nube/detail.html'

# used for displaying a list of user images
class GalleryView(generic.ListView):
    template_name = 'nube/gallery.html'
    context_object_name = 'images'

    # todo: it returns all objects, should return only
    # user's images
    def get_queryset(self):
        return CloudImage.objects.filter()

def get_random_filename(ext):
    """
    Returns a randomly generated string with the specified
    extension `ext` appended at the end. `ext` should have a dot.
    """
    # hex returns a string with no dashes
    return str(uuid.uuid4().hex) + ext
