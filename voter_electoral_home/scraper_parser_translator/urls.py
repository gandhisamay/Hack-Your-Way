from django.urls import include, path
from .views import controllers 

urlpatterns = [
    path('api/', controllers.home, name = 'home'),
    path('api/details', controllers.details, name = 'details'),
    path('api/epic', controllers.epic, name = 'epic'),
]
