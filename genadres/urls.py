#from django.conf.urls import url
from django.urls import path, include 
from .views import GenadresView
from . import views

urlpatterns = [
    path('', views.home, name='home_adreses'),
    path('add-user', views.create_user, name='add_user'),
    path('ajax/save-user', views.save_user, name='save_user'),
    path('get-sheet', views.get_sheet, name='get_sheet'),
    path('genadres/api/', GenadresView.as_view()),
]
