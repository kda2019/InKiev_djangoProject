from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


class Event(models.Model):
    """Публичные события, которыми могут управлять только модераторы"""

    # Обязательные к заполнению поля
    title = models.CharField(max_length=30, verbose_name='Название публичного события')
    text = models.TextField(verbose_name='Текст')
    start_time = models.DateTimeField(verbose_name='Дата начала', db_index=True)

    # Необязательные поля
    image = models.SlugField(blank=True, verbose_name='Картинка')
    end_time = models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания(необязательно)')

    # Технические и автозаполняемые поля
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=True)
    create = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Дата создания')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = GenericRelation("Comment")

    class Meta:
        ordering = ['-start_time']
        verbose_name = 'Событие'
        verbose_name_plural = 'Публичные События'

    def get_class_name(self):
        return self.__class__.__name__


class PrivateEvent(models.Model):
    """Частные события, которые могут добавлять все пользователи"""

    # Обязательные к заполнению поля
    title = models.CharField(max_length=30, verbose_name='Название частного события')
    text = models.TextField(verbose_name='Текст')
    start_time = models.DateTimeField(verbose_name='Дата начала', db_index=True)

    # Необязательные поля
    image = models.SlugField(blank=True, verbose_name='Картинка')
    end_time = models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания(необязательно)')

    # Технические и автозаполняемые поля
    is_active = models.BooleanField(default=True)
    create = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Дата создания')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = GenericRelation("Comment")

    class Meta:
        ordering = ['-start_time']
        verbose_name = 'Событие'
        verbose_name_plural = 'Приватные События'

    def get_class_name(self):
        return self.__class__.__name__


class Place(models.Model):
    """Разнообразные интересные места для проведения своего досуга"""

    # Обязательные к заполнению поля
    title = models.CharField(max_length=30, verbose_name='Название места')
    text = models.TextField(verbose_name='Текст')

    # Необязательные поля
    image = models.SlugField(blank=True, verbose_name='Картинка')

    # Технические и автозаполняемые поля
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=True)
    create = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'

    def get_class_name(self):
        return self.__class__.__name__


class Comment(models.Model):
    """Данный клас реализует коментарии, которые можно связять с любым другим класом
    с помощью полей полиморфной связи
    """

    # Основные поля
    text = models.TextField(verbose_name='Текст', )
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    # Поля для полиморфной связи
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')
