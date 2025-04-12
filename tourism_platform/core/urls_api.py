# core/urls_api.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
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

    # Аутентификация
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Кастомные endpoints
    path('public-routes/', public_routes, name='public-routes'),
    path('user-routes/', user_routes, name='user-routes'),
]

