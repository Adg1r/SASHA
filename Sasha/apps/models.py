"""
Модели для корректной работы сайта и БД.
"""

from django.db import models
from django.contrib.auth.models import User


THEMES = [
    ('primary', 'Стандартный цвет'),
    ('blue', 'Голубой'),
    ('green', 'Зеленый'),
    ('red', 'Карминный'),
    ('indigo', 'Индиго'),
    ('aqua', 'Бирюзовый'),
    ('orange', 'Оранжевый'),
    ('claret', 'Бордовый')
]

BG_THEMES = [
    ('light', 'Светлая'),
    ('dark', 'Тёмная')
]

POST_SORTS = [
    ('name', 'По названию'),
    ('date', 'По дате')
]


class ThemeChanger(models.Model):
    """
    Модель для темы сайта компонентов.
    Имеет два параметра:
    1) главная тема
    2) тема фона
    3) пользователь, использующий тему
    """
    theme = models.CharField(
        max_length=20,
        default='primary',
        choices=THEMES
    )
    background_theme = models.CharField(
        max_length=20,
        default='light',
        choices=BG_THEMES
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )

class EditEmail(models.Model):
    """
    Модель для изменения почтового адреса.
    Изменение происходит с помощью подтверждения по почте.
    Имеет 2 поля:
    1) Пользователь
    2) Почта
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    email = models.EmailField(
        max_length=40
    )


class UserAvatar(models.Model):
    """
    Аватарка для пользователя.
    Имеет два поля:
    1) Пользователь
    2) Аватарка (модель ImageField)
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(upload_to='avatars')
