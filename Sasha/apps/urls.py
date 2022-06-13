from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .themes import THEMES
from .forms import LoginForm


urlpatterns = [
    path('admin/', views.admin_page),
    path('admin/users/', views.admin_opportunity_users),
    path('admin/make-admin/<int:user_id>', views.admin_make_admin),
    path('admin/make-user/<int:user_id>', views.admin_make_user),
    path('admin/block-user/<int:user_id>', views.block_user),
    path('admin/unblock-user/<int:user_id>', views.unblock_user),
    path('', views.index_page),
    path('api/', views.api),
    path('profile/', views.profile_edit_page),
    path('profile/edit/confirm/<uidb64>/<token>/', views.profile_edit_confirm_page, name='edit_confirm'),
    path('profile/reg/', views.profile_reg_page),
    path('profile/activate/<uidb64>/<token>/', views.profile_activate_page, name='account_activate'),
    path('profile/logout/', views.profile_logout_page),
    path('profile/login/', views.profile_login_page),
    path('profile/themes/', views.theme_changer_page),
    path('profile/password/',views. change_password_page),
    path('profile/accounts/', views.accounts),
    path('profile/avatar/', views.upload_avatar),
    path('profile/avatar/remove/', views.remove_avatar),
    path('reset-password/', auth_views.PasswordResetView.as_view(
        email_template_name='password_reset/email.html',
        template_name='password_reset/form.html',
        extra_context={'theme': THEMES['primary'], 'bg_theme': 'light', 'login_form': LoginForm()},
        success_url='/reset-password/done',
        subject_template_name='password_reset/email_title.txt'
    )),
    path('reset-password/done', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset/done.html',
        extra_context={'theme': THEMES['primary'], 'bg_theme': 'light', 'login_form': LoginForm()},
    )),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset/confirm.html',
        success_url='/reset/done',
        extra_context={'theme': THEMES['primary'], 'bg_theme': 'light', 'login_form': LoginForm()},
    ), name='reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset/complete.html',
        extra_context={'theme': THEMES['primary'], 'bg_theme': 'light', 'login_form': LoginForm()},
    )),
    path('works/', views.get_works),
    path('equations/', views.get_equations),
    path('works/show/', views.show_product)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)