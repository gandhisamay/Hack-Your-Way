from django.urls import include, path
from . import views as controllers

urlpatterns = [
    path('home/', controllers.home, name = 'home'),
    path('sikkim/', controllers.sikkim, name = 'sikkim'),
]
