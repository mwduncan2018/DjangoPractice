from django.urls import path

from . import views


app_name = 'messageboard'
urlpatterns = [
    #path(r'<int:question_id>/', views.detail, name='detail'),
    path(r'about/', views.about, name='about'),
    path(r'addpost/', views.add_post, name='add_post'),
    path(r'clearconversation/', views.clear_conversation, name='clear_conversation'),
    path(r'viewanimals/', views.view_animals, name='view_animals'),
    path(r'chat/', views.animal_conversation, name='animal_conversation'),
    path(r'', views.splash, name='splash'),
]