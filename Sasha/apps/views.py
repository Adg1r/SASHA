"""
Модуль с функциями-обработчиками страниц.
"""
import datetime
import json
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import update_session_auth_hash, logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from .forms import LoginForm, RegistrationForm, ThemeForm,\
    ProfileEditForm, PasswordEditForm, SearchUser, AccountsForm, \
    CreateCanalForm, AddUserToCanal, EditArticleForm, \
    NewPostForm, FilterPostForm, AddImageUser, SearchPostForm, SearchCanalForm
from .tokens import CONFIRM_TOKEN
from .themes import THEMES
from . import models


def admin_required(function):
    """
    Декоратор для проверки is_superuser и is_staff.
    :param function: функция
    :return: функция или перенаправление на главную страницу
    """
    def inner(request, *args, **kwargs):
        if request.user.is_superuser and request.user.is_staff:
            return function(request, *args, **kwargs)
        messages.add_message(request, messages.ERROR, "Недостаточно прав.")
        return redirect('/')
    return inner


def get_base_context(request):
    """
    Получение базового контекста.
    :param request: объект запроса
    :return: базовый контекст
    """
    context = dict()
    if request.user.is_authenticated:
        try:
            theme_model = models.ThemeChanger.objects.get(user=request.user)
        except ObjectDoesNotExist:
            theme_model = models.ThemeChanger(
                theme='primary', background_theme='light', user=request.user
            )
            theme_model.save()

        try:
            avatar = models.UserAvatar.objects.get(user=request.user)
            context['avatar'] = avatar.image.url
            context['default_avatar'] = False
        except ObjectDoesNotExist:
            context['avatar'] = '/static/default.jpg'
            context['default_avatar'] = True
        context['theme'] = THEMES[theme_model.theme]
        context['bg_theme'] = theme_model.background_theme
    else:
        context['theme'] = THEMES['primary']
        context['bg_theme'] = 'light'
    context['user'] = request.user
    context['login_form'] = LoginForm()
    return context


def get_base_admin_context():
    """
    Получение базового контекста администратора.
    :return: базовый контекст администратора
    """
    opportunities = [
        dict(name='Управление пользователями', url='/admin/users/')
    ]
    return opportunities


def index_page(request):
    """
    Главная страница сайта.
    :param request: объект запроса
    :return: объект ответа сервера с HTML
    """
    context = get_base_context(request)
    return render(request, 'index.html', context)


def profile_reg_page(request):
    """
    Страница регистрации пользователя.
    :param request: объект запроса
    :return render: объект ответа сервера с HTML
    :return redirect: перенаправление на главную страницу сайта
    """
    if not request.user.is_authenticated:
        context = get_base_context(request)
        context['reg_form'] = RegistrationForm()
        if request.method == 'POST':
            reg_form = RegistrationForm(request.POST)
            context['reg_form'] = reg_form
            if reg_form.is_valid():
                username = reg_form.data['username']
                password = reg_form.data['password']
                first_name = reg_form.data['first_name']
                last_name = reg_form.data['last_name']
                email = reg_form.data['email']
                if not User.objects.filter(username=username).exists():
                    if not User.objects.filter(email=email).exists():
                        user = User.objects.create_user(username, email, password)
                        user.first_name = first_name
                        user.last_name = last_name
                        user.is_active = False
                        user.save()
                        theme = models.ThemeChanger(
                            theme='primary', background_theme='light', user=user
                        )
                        theme.save()

                        current_site = get_current_site(request)
                        mail_subject = 'Активация аккаунта на сайте Sasha'
                        message = render_to_string('registration/reg_confirm_email.html', {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': CONFIRM_TOKEN.make_token(user),
                        })
                        email_message = EmailMessage(
                            mail_subject, message, to=[reg_form.data['email']]
                        )
                        email_message.send()
                        messages.add_message(
                            request, messages.INFO,
                            "Мы отправили Вам письмо с инструкцией для активации аккаунта."
                            " В данный момент доступ к Вашему аккаунту ограничен."
                        )
                        return redirect('/')
                    messages.add_message(request, messages.ERROR,
                                         "Выбранная почта привязана к другому аккаунту.")
                else:
                    messages.add_message(request, messages.ERROR,
                                         "Пользователь с таким логином уже существует.")
            else:
                messages.add_message(request, messages.ERROR,
                                     "Некорректные данные в форме регистрации.")
        return render(request, 'registration/reg.html', context)
    messages.add_message(request, messages.WARNING, "Вы уже зарегистрированы.")
    return redirect('/')


def profile_activate_page(request, uidb64, token):
    """
    Страница подтверждения регистрации профиля.
    :param request: объект запроса
    :param uidb64: закодированный ключ
    :param token: токен
    :return redirect: перенаправление на главную страницу
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, ObjectDoesNotExist):
        user = None
    if user is not None and CONFIRM_TOKEN.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.add_message(request, messages.SUCCESS, "Вы успешно зарегистрировались.")
    else:
        messages.add_message(request, messages.ERROR,
                             "Не удалось подтвердить регистрацию аккаунта.")
    return redirect('/')


@login_required
def profile_edit_page(request):
    """
    Страница изменения данных пользователя.
    :param request: объект запроса
    :return render: объект ответа сервера с HTML
    :return redirect: перенаправление на эту же страницу
    """
    context = get_base_context(request)
    context['edit_form'] = ProfileEditForm(initial={
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
    })
    if request.method == 'POST':
        edit_form = ProfileEditForm(request.POST)
        context['edit_form'] = edit_form
        if edit_form.is_valid():
            if request.user.first_name != edit_form.data['first_name'] or \
                    request.user.last_name != edit_form.data['last_name'] or \
                    request.user.email != edit_form.data['email']:
                if not User.objects.filter(email=edit_form.data['email']).exists() or \
                        request.user.email == edit_form.data['email']:
                    request.user.first_name = edit_form.data['first_name']
                    request.user.last_name = edit_form.data['last_name']
                    request.user.save()
                    if request.user.email != edit_form.data['email']:
                        current_site = get_current_site(request)
                        mail_subject = 'Изменение почтового адреса на сайте Reader'
                        message = render_to_string('registration/edit_confirm_email.html', {
                            'user': request.user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
                            'token': CONFIRM_TOKEN.make_token(request.user),
                        })
                        email_message = EmailMessage(
                            mail_subject, message, to=[edit_form.data['email']]
                        )
                        email_message.send()
                        edit_email = models.EditEmail(
                            user=request.user, email=edit_form.data['email']
                        )
                        edit_email.save()
                        messages.add_message(request, messages.INFO,
                                             "Мы отправили Вам на почту письмо"
                                             " с инструкциями для изменения E-mail."
                                             " Остальные данные были успешно изменены")
                    else:
                        messages.add_message(request, messages.SUCCESS,
                                             "Вы успешно изменили данные профиля.")
                    return redirect('/profile/')
                messages.add_message(request, messages.ERROR,
                                     "Выбранная почта привязана к другому аккаунту.")
            else:
                messages.add_message(request, messages.WARNING,
                                     "Новые данные профиля совпадают со старыми.")
        else:
            messages.add_message(request, messages.ERROR,
                                 "Некорректные данные в форме.")
    return render(request, 'registration/edit.html', context)


def profile_edit_confirm_page(request, uidb64, token):
    """
    Страница подтверждения изменения E-mail.
    :param request: объект запроса
    :param uidb64: закодированный ключ
    :param token: токен
    :return redirect: перенаправление на страницу редактирования профиля
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, ObjectDoesNotExist):
        user = None
    if user is not None and CONFIRM_TOKEN.check_token(user, token):
        try:
            edit_email = models.EditEmail.objects.get(user=user)
            user.email = edit_email.email
            user.save()
            edit_email.delete()
            messages.add_message(request, messages.SUCCESS, "Вы успешно изменили E-mail.")
        except ObjectDoesNotExist:
            messages.add_message(request, messages.ERROR,
                                 "Не удалось изменить E-mail.")
    else:
        messages.add_message(request, messages.ERROR,
                             "Не удалось изменить E-mail.")
    return redirect('/profile')


@login_required
def change_password_page(request):
    """
    Страница смены пароля пользователя.
    :param request: объект запроса
    :return: объект ответа сервера с HTML
    """
    context = get_base_context(request)
    context['password_edit'] = PasswordEditForm()
    if request.method == 'POST':
        password_edit_form = PasswordEditForm(request.POST)
        if password_edit_form.is_valid():
            old_password = password_edit_form.data['old_password']
            if request.user.check_password(old_password):
                new_password = password_edit_form.data['new_password']
                password_confirmation = password_edit_form.data['password_confirmation']
                if new_password == password_confirmation:
                    if new_password != old_password:
                        request.user.set_password(new_password)
                        request.user.save()
                        update_session_auth_hash(request, request.user)
                        messages.add_message(request, messages.SUCCESS,
                                             "Вы успешно изменили пароль.")
                    else:
                        messages.add_message(request, messages.WARNING,
                                             "Новый пароль совпадает со старым.")
                else:
                    messages.add_message(request, messages.ERROR, "Пароли не совпадают.")
            else:
                messages.add_message(request, messages.ERROR, "Неправильный текущий пароль.")
        else:
            messages.add_message(request, messages.ERROR,
                                 "Некорректные данные в форме смены пароля.")
    return render(request, "registration/password_edit.html", context)


def profile_login_page(request):
    """
    Авторизация пользователя на сайте.
    Не имеет своей страницы.
    :param request: объект запроса
    :return: перенаправление на главную страницу
    """
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.data['username']
            password = login_form.data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, "Авторизация успешна.")
            else:
                try:
                    selected_user = User.objects.get(username=username)
                    if selected_user.is_active:
                        messages.add_message(request, messages.ERROR,
                                             "Неправильный логин или пароль.")
                    else:
                        messages.add_message(request, messages.ERROR,
                                             "Данный пользователь заблокирован.")
                except ObjectDoesNotExist:
                    messages.add_message(request, messages.WARNING,
                                         "Пользователя с таким логином не существует,"
                                         " но вы можете стать им :)")
        else:
            messages.add_message(request, messages.ERROR,
                                 "Некорректные данные в форме авторизации.")
    return redirect('/')


@login_required
def profile_logout_page(request):
    """
    Деавторизация пользователя.
    Не имеет своей страницы.
    :param request: объект запроса
    :return: перенаправление на главную страницу
    """
    logout(request)
    messages.add_message(request, messages.SUCCESS, "Вы успешно вышли из аккаунта")
    return redirect('/')


@login_required
def theme_changer_page(request):
    """
    Страница смены темы сайта.
    Тема привязывается к аккаунту на сайте.
    :param request: объект запроса
    :return render: объект ответа сервера с HTML
    :return redirect: перенаправление на эту же страницу
    """
    context = get_base_context(request)
    theme = models.ThemeChanger.objects.get(user=request.user)
    context['theme_form'] = ThemeForm(
        initial={'theme': theme.theme, 'bg_theme': theme.background_theme}
    )
    if request.method == 'POST':
        theme_form = ThemeForm(request.POST)
        if theme_form.is_valid():
            theme_changer = models.ThemeChanger.objects.get(user=request.user)
            theme_changer.theme = theme_form.data['theme']
            theme_changer.background_theme = theme_form.data['bg_theme']
            theme_changer.save()
            return redirect('/profile/themes')
    return render(request, 'themes.html', context)


@admin_required
@login_required
def admin_page(request):
    """
    Страница с возможностями для администраторов.
    :param request: объект запроса
    :return render: объект ответа сервера с HTML
    :return redirect: перенаправление на главную страницу
    """
    context = get_base_context(request)
    context['opportunities'] = get_base_admin_context()
    return render(request, 'admin/admin_page.html', context)


@admin_required
@login_required
def admin_opportunity_users(request):
    """
    Управление пользователями.
    :param request: объект запроса
    :return render: объект ответа сервера с HTML
    :return redirect: перенаправление на главную страницу
    """
    context = get_base_context(request)
    context['all_users'] = User.objects.all()
    context['search_user'] = SearchUser()
    if request.method == 'POST':
        search_user = SearchUser(request.POST)
        context['search_user'] = search_user
        if search_user.is_valid():
            context['all_users'] = User.objects.filter(username__contains=search_user.data['user'])
    return render(request, 'admin/admin_op_users.html', context)


@admin_required
@login_required
def admin_make_admin(request, user_id):
    """
    Делает пользователя superuser'ом.
    :param request: объект запроса
    :param user_id: ID пользователя
    :return:
    """
    selected_user = User.objects.get(id=user_id)
    selected_user.is_superuser = 1
    selected_user.is_staff = 1
    selected_user.save()
    print(request)
    return redirect('/admin/users')


@admin_required
@login_required
def admin_make_user(request, user_id):
    """
    Понижает до пользователя.
    :param request: объект запроса
    :param user_id: ID пользователя
    :return:
    """
    selected_user = User.objects.get(id=user_id)
    selected_user.is_superuser = 0
    selected_user.is_staff = 0
    selected_user.save()
    print(request)
    return redirect('/admin/users')


@admin_required
@login_required
def block_user(request, user_id):
    """
    Блокирует пользователя.
    :param request: объект запроса
    :param user_id: ID пользователя
    :return redirect: перенаправление на страницу
    """
    selected_user = User.objects.get(id=user_id)
    selected_user.is_active = 0
    selected_user.save()
    print(request)
    return redirect('/admin/users')

@login_required
def get_works(request):
    """
    Страница готовых работ
    :param request: объекст запроса
    :param render: объект ответа сервера HTML
    """
    context = get_base_context(request)
    return render(request, 'works.html', context)

@login_required
def show_product(request):
    """
    Страница готовых работ
    :param request: объекст запроса
    :param render: объект ответа сервера HTML
    """
    context = get_base_context(request)
    return render(request, 'show.html', context)

@login_required
def get_equations(request):
    """
    Страница готовых работ
    :param request: объекст запроса
    :param render: объект ответа сервера HTML
    """
    context = get_base_context(request)
    return render(request, 'equations.html', context)
