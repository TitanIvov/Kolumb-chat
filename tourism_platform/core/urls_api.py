# core/urls_api.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    RouteViewSet,
    PointViewSet,
    public_routes,
    user_routes,
)

# Инициализация роутера
router = DefaultRouter()

# Регистрация ViewSets
router.register(r'users', UserViewSet, basename='user')
router.register(r'routes', RouteViewSet, basename='route')
router.register(r'points', PointViewSet, basename='point')

# Дополнительные API endpoints
urlpatterns = [
    # Основные CRUD endpoints через роутер
    path('', include(router.urls)),


    # Кастомные endpoints
    path('public-routes/', public_routes, name='public-routes'),
    path('user-routes/', user_routes, name='user-routes'),
]



