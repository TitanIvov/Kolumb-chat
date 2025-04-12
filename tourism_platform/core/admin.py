from django.contrib import admin
from .models import Route, Point  

@admin.register(Route)  
class RouteAdmin(admin.ModelAdmin):  
    list_display = ("title", "creator", "is_public", "created_at")  
    search_fields = ("title", "creator__username")  

@admin.register(Point)  
class PointAdmin(admin.ModelAdmin):  
    list_display = ("name", "route", "latitude", "longitude")  
    search_fields = ("name", "route__title")  
# Register your models here.
