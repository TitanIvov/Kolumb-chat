# core/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import json

class CustomUser(AbstractUser):
    # Дополнительные поля для пользователя
    nickname = models.CharField(max_length=50, unique=True, verbose_name="Никнейм")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name="Пол")
    bio = models.TextField(blank=True, verbose_name="О себе")
    country = models.CharField(max_length=100, blank=True, verbose_name="Страна")
    city = models.CharField(max_length=100, blank=True, verbose_name="Город")
    language = models.CharField(max_length=50, default='Русский', verbose_name="Язык")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    last_login = models.DateTimeField(auto_now=True, verbose_name="Последний вход")
    followers = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='following', verbose_name="Подписчики")
    friends = models.ManyToManyField('self', blank=True, verbose_name="Друзья")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.nickname

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название тега")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Route(models.Model):
    ACTIVITY_TYPES = [
        ('walking', 'Пеший'),
        ('cycling', 'Велосипедный'),
        ('driving', 'Автомобильный'),
    ]

    title = models.CharField(max_length=200, verbose_name="Название")
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_routes',
        verbose_name="Создатель"
    )
    categories = models.ManyToManyField(Category, verbose_name="Категории")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги")
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=200, blank=True, verbose_name="Улица")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    difficulty = models.PositiveIntegerField(
        verbose_name="Уровень сложности",
        help_text="От 1 до 5"
    )
    min_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0, 
        verbose_name="Минимальная цена"
    )
    max_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0, 
        verbose_name="Максимальная цена"
    )
    rating = models.FloatField(default=0, verbose_name="Рейтинг")
    completions = models.PositiveIntegerField(default=0, verbose_name="Пройдено раз")
    metadata = models.JSONField(default=dict, blank=True, verbose_name="Метаданные")
    status = models.BooleanField(default=True, verbose_name="Публичный статус")
    duration = models.DurationField(verbose_name="Время прохождения")
    start_point = models.ForeignKey(
        'Point',
        on_delete=models.SET_NULL,
        null=True,
        related_name='start_routes',
        verbose_name="Начальная точка"
    )
    end_point = models.ForeignKey(
        'Point',
        on_delete=models.SET_NULL,
        null=True,
        related_name='end_routes',
        verbose_name="Конечная точка"
    )
    distance = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        verbose_name="Протяженность (км)"
    )
    activity_type = models.CharField(
        max_length=20,
        choices=ACTIVITY_TYPES,
        default='walking',
        verbose_name="Тип активности"
    )

    class Meta:
        verbose_name = "Маршрут"
        verbose_name_plural = "Маршруты"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.city}, {self.country})"

class Point(models.Model):
    POINT_TYPES = [
        ('restaurant', 'Ресторан'),
        ('hotel', 'Отель'),
        ('waterfall', 'парк'),
        ('monument', 'Достопримечательность'),
        ('other', 'Другое'),
    ]

    latitude = models.FloatField(verbose_name="Широта")
    longitude = models.FloatField(verbose_name="Долгота")
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    point_type = models.CharField(
        max_length=20,
        choices=POINT_TYPES,
        default='other',
        verbose_name="Тип точки"
    )
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги")
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=200, verbose_name="Улица")
    house = models.CharField(max_length=20, blank=True, verbose_name="Дом")
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_points',
        verbose_name="Создатель"
    )
    is_verified = models.BooleanField(default=False, verbose_name="Подтвержденная локация")
    working_hours = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="График работы",
        help_text="JSON-структура с расписанием"
    )
    min_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0, 
        verbose_name="Минимальная цена"
    )
    max_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0, 
        verbose_name="Максимальная цена"
    )
    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Метаданные",
        help_text="Фото/видео в формате JSON"
    )
    visits = models.PositiveIntegerField(default=0, verbose_name="Отметок 'здесь был'")
    rating = models.FloatField(default=0, verbose_name="Рейтинг")
    status = models.BooleanField(default=True, verbose_name="Публичный статус")
    routes = models.ManyToManyField(
        Route,
        related_name='points',
        blank=True,
        verbose_name="Маршруты"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Точка интереса"
        verbose_name_plural = "Точки интереса"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.city}, {self.country})"

    def save(self, *args, **kwargs): # Автоматическое заполнение страны/города из маршрута при создании
        if self.routes.exists() and not self.country:
            main_route = self.routes.first()
            self.country = main_route.country
            self.city = main_route.city
        super().save(*args, **kwargs)