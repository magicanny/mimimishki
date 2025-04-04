import os
from uuid import uuid4

from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import UniqueConstraint, Q
from django.urls import reverse
from django.utils import timezone


def get_image_path(instance, filename):
    """
    Generate uuid-name and file path for new post's image
    """
    extension = filename.split('.')[-1]
    filename = "%s.%s" % (uuid4().hex[:16], extension)
    return os.path.join(f'images/posts/{instance.post.created_date:%Y/%m/%d}', filename)


class Image(models.Model):

    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post_images')
    img = models.ImageField(upload_to=get_image_path, blank=True, verbose_name='Изображение',
                            validators=[FileExtensionValidator(
                                allowed_extensions=('png', 'jpg', 'jpeg', 'gif')
                            )])
    is_main = models.BooleanField(default=False, verbose_name='Главное изображение')
    title = models.CharField(max_length=100, verbose_name='Заголовок', blank=True)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        constraints = [
            UniqueConstraint(fields=('post_id',),
                             condition=Q(is_main=True),
                             name='unique_is_main',
                             violation_error_message='Выберите только одно главное изображение')
        ]

    def __str__(self):
        return self.title or f'Изображение к посту "{self.post.title}"'


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор',
                               related_name='blog_posts', editable=False)
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.SlugField(max_length=100, unique=True,
                            help_text='Значение генерируется автоматически на основе заголовка')
    body = models.TextField(verbose_name='Содержание')
    status = models.IntegerField(choices=Status.choices, default=Status.DRAFT, verbose_name='Статус записи')
    published_date = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING, related_name='posts',
                                 verbose_name='Категория', blank=True, null=True)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-created_date',)
        get_latest_by = ('published_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название категории')
    slug = models.SlugField(max_length=150, verbose_name='URL категории',
                            help_text='Значение генерируется автоматически на основе заголовка')
    description = models.TextField(max_length=300, verbose_name='Описание категории', blank=True, null=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('blog:post_category', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title