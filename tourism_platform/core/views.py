# core/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Route, Point
from .serializers import (
    UserSerializer,
    RouteSerializer,
    PointSerializer,
    RouteDetailSerializer
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.decorators import api_view


User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser] 

class RouteViewSet(viewsets.ModelViewSet):
    serializer_class = RouteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Route.objects.filter(
            creator=self.request.user
        ) | Route.objects.filter(is_public=True)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RouteDetailSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=['POST'])
    def add_point(self, request, pk=None):
        route = self.get_object()
        serializer = PointSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(route=route)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PointViewSet(viewsets.ModelViewSet):
    serializer_class = PointSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Point.objects.filter(route__creator=self.request.user)

    def perform_create(self, serializer):
        route = serializer.validated_data['route']
        if route.creator != self.request.user:
            raise permissions.PermissionDenied("Вы не являетесь создателем этого маршрута")
        serializer.save()


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def public_routes(request):
    routes = Route.objects.filter(is_public=True)
    serializer = RouteSerializer(routes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_routes(request):
    routes = Route.objects.filter(creator=request.user)
    serializer = RouteSerializer(routes, many=True)
    return Response(serializer.data)