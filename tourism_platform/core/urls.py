from django.urls import path
from .views import route_list  # Импорт функции

urlpatterns = [
    path('routes/', route_list, name='route-list'),
]
