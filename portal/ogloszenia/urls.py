from django.urls import path
from . import views

# definicje listy url

urlpatterns = [
    path('', views.index)
]
