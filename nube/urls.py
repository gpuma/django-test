from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'nube'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', auth_views.login, {
         'template_name': 'nube/login.html'}, name='login'),
    path('logout', auth_views.logout, {
         'template_name': 'nube/logout.html'}, name='logout'),
    path('create', views.create, name='create'),
    path('img/<int:pk>/', views.ImageDetailView.as_view(), name='detail'),
    path('all', views.GalleryView.as_view(), name='gallery'),
]
