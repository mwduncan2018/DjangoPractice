from django.urls import path

from . import views


app_name = 'messageboard'
urlpatterns = [
    #path(r'<int:question_id>/', views.detail, name='detail'),
    path(r'about/', views.about, name='about'),
    path(r'add/', views.add_post, name='add_post'),
    path(r'clear/', views.clear_conversation, name='clear_conversation'),
    path(r'animals/', views.view_animals, name='view_animals'),
    path(r'conversation/', views.animal_conversation, name='animal_conversation'),
    path(r'', views.splash, name='splash'),
]