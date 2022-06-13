# Generated by Django 3.1.4 on 2020-12-13 10:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Canals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=50)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EditEmail',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('email', models.EmailField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='FilterPost',
            fields=[
                ('post_sort', models.CharField(choices=[('name', 'По названию'), ('date', 'По дате')], default='date', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(max_length=50)),
                ('link', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ThemeChanger',
            fields=[
                ('theme', models.CharField(choices=[('primary', 'Стандартный цвет'), ('blue', 'Голубой'), ('green', 'Зеленый'), ('red', 'Карминный'), ('indigo', 'Индиго'), ('aqua', 'Бирюзовый'), ('orange', 'Оранжевый'), ('claret', 'Бордовый')], default='primary', max_length=20)),
                ('background_theme', models.CharField(choices=[('light', 'Светлая'), ('dark', 'Тёмная')], default='light', max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='UserAvatar',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('image', models.ImageField(upload_to='avatars')),
            ],
        ),
        migrations.CreateModel(
            name='UserCanals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('canal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.canals')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserAccounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_tg', models.CharField(max_length=512)),
                ('user_vk', models.CharField(max_length=512)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SavedPosts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('title', models.CharField(default='', max_length=512)),
                ('url', models.CharField(max_length=512)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostsTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=256)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.savedposts')),
            ],
        ),
        migrations.CreateModel(
            name='PostsCanals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('canal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.canals')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.savedposts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LikesPostInCanals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.postscanals')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
