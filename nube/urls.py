from django.urls import path

from . import views

app_name = 'nube'
urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('img/<int:pk>/', views.ImageDetailView.as_view(), name='detail'),
    path('all', views.GalleryView.as_view(), name='gallery'),
    path('ajax/dummy/', views.dummy_image, name = 'dummy'),
]
