from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

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
    path('all', login_required(views.GalleryView.as_view()), name='gallery'),
    path('save', views.save_img, name='save'),
    path('signup', views.signup, name='signup'),
]
