from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('nube/', include('nube.urls')),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
