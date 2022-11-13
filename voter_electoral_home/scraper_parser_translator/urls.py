from django.urls import include, path
from .views import controllers 

urlpatterns = [
    path('api/', controllers.home, name = 'home'),
    path('api/details', controllers.sikkim, name = 'details'),
    path('api/epic', controllers.sikkim, name = 'epic'),
]
