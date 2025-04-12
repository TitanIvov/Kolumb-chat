from django.contrib import admin
from .models import Route, Point

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    pass

@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    pass