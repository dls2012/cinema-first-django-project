from django.contrib.auth.models import User
from django.db import models

# Create your models here.

# Класс созданный в model.py является моделью связующей с таблицей БД

# Модель категории
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название категории')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'


# Модель кинофильмов
class Cinema(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название кинофильма')
    content = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name='Картинка')  # blank=True, null=True - говорим что поле не обязательное для заполнения
    video = models.FileField(upload_to='videos/', blank=True, null=True, verbose_name='Видео')
    trailer = models.FileField(upload_to='trailers/', blank=True, null=True, verbose_name='Треилер')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Автор')

    def __str__(self):
        return self.title

    def get_views(self):  # Метод который вернёт количество просмотров кинофильма
        if self.views:
            return self.views.count()
        else:
            return 0


    class Meta:
        verbose_name = 'Кинофильм'
        verbose_name_plural = 'Кинофильмы'

    def get_photo(self):  # Метод для получения картинки объекта
        if self.image:
            return self.image.url
        else:
            return 'https://zbs-shina.ru/image/trumb/700x700/1954516UniroyalRainSport3FQ2.jpg'


    #  Умная ссылка
    def get_absolute_url(self):
        return reverse('cinema', kwargs={'pk': self.pk})



class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, verbose_name='Кинофильм')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата Добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True, verbose_name='Фото профиля')
    publisher = models.BooleanField(default=True, verbose_name='Право на публикации')
    about = models.CharField(max_length=200, blank=True, null=True, verbose_name='О пользователе')
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True, verbose_name='Город пользователя')


    def __str__(self):
        return self.user.first_name

    def get_profile_photo(self):  # Метод для получения аватрки профиля
        if self.photo:
            return self.photo.url
        else:
            return 'https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava3.webp'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'



class City(models.Model):
    city_name = models.CharField(max_length=150, verbose_name='Города')

    def __str__(self):
        return self.city_name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


# Меодель для хранения IP
class Ip(models.Model):
    ip = models.CharField(max_length=100, verbose_name='Адрес Ip')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пользователь')
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, verbose_name='Кинофильм', related_name='views')

    def __str__(self):
        return f'Ip: {self.ip} на кинофильм {self.cinema.title}'

    class Meta:
        verbose_name = 'Ip Пользователя'
        verbose_name_plural = 'Ip пользователей'


