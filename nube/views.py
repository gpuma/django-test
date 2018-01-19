from django.shortcuts import render
from django.views import generic
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse  # for AJAX
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from requests.exceptions import MissingSchema

from .word_cloud import WordCloud
from .models import CloudImage
from .constants import *
# celery task test
from nube.tasks import create_word_cloud_task


def index(request):
    return render(request, 'nube/index.html')


def create(request):
    """
    Displays the generated WordCloud from the
    given URI or uploaded file
    """
    # in order to avoid KeyError
    myfile = request.FILES.get('myfile', None)

    if request.POST['uri'] == '' and myfile is None:
        return render(request, 'nube/index.html', {
            'error_message': NOTHING_TO_PROCESS
        })
    try:
        # todo: making a task synchronous (.get()) is not the recommended way of using celery
        # have to research more on how to do this properly
        if myfile:
            content = myfile
            type = "upload"
        else:
            content = request.POST['uri']
            type = "internet"
        # main operation
        filename = create_word_cloud_task.delay(content, type, settings.MEDIA_ROOT).get(timeout=60)
    except MissingSchema:
        # todo: this might need a redirect instead
        return render(request, 'nube/index.html', {
            'error_message': URI_COULD_NOT_BE_PROCESSED
        })
    else:
        return JsonResponse({
            'img_filename': filename,
        })


@login_required
def save_img(request):
    # todo: needs some try catch
    img = CloudImage(image=request.POST['img_filename'],
                     creation_date=timezone.now(),
                     name=request.POST['img_name'],
                     user_id=request.user.id)
    img.save()
    return HttpResponseRedirect(reverse('nube:gallery'))


# used for displaying a list of user images
class GalleryView(generic.ListView):
    template_name = 'nube/gallery.html'
    context_object_name = 'images'

    def get_queryset(self):
        return CloudImage.objects.filter(user_id=self.request.user.id)


class ImageDetailView(generic.DetailView):
    model = CloudImage
    template_name = 'nube/detail.html'
