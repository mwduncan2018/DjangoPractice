from django.urls import path

from . import views


app_name = 'messageboard'
urlpatterns = [
    #path(r'<int:question_id>/', views.detail, name='detail'),
    path(r'create/', views.create, name='create'),
    path(r'edit/<int:id>/', views.edit, name='edit'),
    path(r'details/<int:id>/', views.details, name='details'),
    path(r'delete/<int:id>/', views.delete, name='delete'),
    path(r'', views.index, name='index'),
]