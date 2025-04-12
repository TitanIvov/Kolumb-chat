from django.db import models
from django.contrib.auth.models import AbstractUser  
from django.contrib.auth.models import User
from django.conf import settings


class CustomUser(AbstractUser):  
    bio = models.TextField(blank=True, null=True)  # Опциональное поле  

class Route(models.Model):  
    title = models.CharField(  
        max_length=200,  
        verbose_name="Название маршрута"  
    )  
    description = models.TextField(  
        verbose_name="Описание",  
        blank=True,  
        null=True  
    )

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Создатель"
    )
    is_public = models.BooleanField(  
        default=False,  
        verbose_name="Публичный"  
    )  
    created_at = models.DateTimeField(  
        auto_now_add=True,  
        verbose_name="Дата создания"  
    )  
    def __str__(self):  
        return self.title  
    
class Point(models.Model):  
    name = models.CharField(  
        max_length=100,  
        verbose_name="Название точки"  
    )  
    latitude = models.FloatField(  
        verbose_name="Широта"  
    )  
    longitude = models.FloatField(  
        verbose_name="Долгота"  
    )  
    route = models.ForeignKey(  
        Route,  
        on_delete=models.CASCADE,  
        related_name="points",  
        verbose_name="Маршрут"  
    )  

    def __str__(self):  
        return f"{self.name} ({self.latitude}, {self.longitude})"  
    

