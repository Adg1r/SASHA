"""
Формы для получения входных данных.
"""
from django import forms
from django.core.files.images import get_image_dimensions
from .models import THEMES, BG_THEMES, POST_SORTS


SEARCH_TAGS_TYPE = [
    ('and', 'И'),
    ('or', 'Или')
]


class LoginForm(forms.Form):
    """
    Форма авторизации пользователя.
    """
    username = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Логин: ',
            }
        )
    )
    password = forms.CharField(
        max_length=20,
        min_length=3,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Пароль: ',
            }
        )
    )


class RegistrationForm(forms.Form):
    """
    Форма регистрации пользователя.
    """
    first_name = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Имя'
    )
    last_name = forms.CharField(
        max_length=40,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Фамилия'
    )
    email = forms.CharField(
        max_length=40,
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label='E-mail'
    )
    username = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Логин'
    )
    password = forms.CharField(
        max_length=20,
        min_length=3,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Пароль'
    )


class ProfileEditForm(forms.Form):
    """
    Форма редактирования основных данных профиля пользователя.
    """
    first_name = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Имя'
    )
    last_name = forms.CharField(
        max_length=40,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Фамилия'
    )
    email = forms.CharField(
        max_length=40,
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label='E-mail'
    )


class PasswordEditForm(forms.Form):
    """
    Форма смены пароля пользователя.
    """
    old_password = forms.CharField(
        max_length=20,
        min_length=3,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Текущий пароль'
    )

    new_password = forms.CharField(
        max_length=20,
        min_length=3,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Новый пароль'
    )

    password_confirmation = forms.CharField(
        max_length=20,
        min_length=3,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Новый пароль ещё раз'
    )


class ThemeForm(forms.Form):
    """
    Форма выбора темы сайта.
    """
    bg_theme = forms.ChoiceField(
        label='Основная тема',
        choices=BG_THEMES,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )
    theme = forms.ChoiceField(
        label='Цвет компонентов',
        choices=THEMES,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

class AddImageUser(forms.Form):
    """
    Форма добавления изображения пользователем.
    """
    image = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'custom-file-input'
            }
        )
    )

    def check_resolution(self):
        """
        Проверяет разрешение изображения.
        :return True: если разрешение меньше 800x800
        :return False: если разрешение больше 800x800
        """
        image = self.cleaned_data['image']
        width, height = get_image_dimensions(image)
        if width > 1600 or height > 1600:
            return False
        return True

    def check_size(self):
        """
        Проверяет размер изображения.
        :return True: если размер меньше 200 КБ
        :return False: если размер больше 200 КБ
        """
        image = self.cleaned_data['image']
        print(len(image))
        if len(image) > 2* 1024 * 1024:
            return False
        return True

    def check_content(self):
        """
        Проверяет тип изображения.
        :return True: если png или jpeg
        :return False: если любой другой тип
        """
        image = self.cleaned_data['image']
        main, sub = image.content_type.split('/')
        print(main, sub)
        if main == 'image' and (sub in ['jpeg', 'png']):
            return True
        return False