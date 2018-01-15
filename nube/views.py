from django.shortcuts import render
from django.views import generic

#class IndexView(generic.FormView):
    #template_name = 'nube/index.html'

def index(request):
    # todo: turn this into a generic view?
    return render(request, 'nube/index.html')

def create(request):
    # todo: pending
    return render(request, None)
