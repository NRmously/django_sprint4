from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class IsPublishedModel(models.Model):
    """Абстрактная модель. Добвляет флаг is_published"""

    is_published = models.BooleanField(
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.',
        verbose_name='Опубликовано'
    )

    class Meta:
        abstract = True


class CreatedAtModel(models.Model):
    """Абстрактная модель. Добвляет флаг created_at"""

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True
        ordering = ('created_at', )


class Location(IsPublishedModel, CreatedAtModel):
    name = models.CharField(
        max_length=settings.MAX_STRING_LENGTH,
        verbose_name='Название места',
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(IsPublishedModel, CreatedAtModel):
    title = models.CharField(
        max_length=settings.MAX_STRING_LENGTH,
        verbose_name='Заголовок'
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        help_text='Идентификатор страницы для URL; разрешены символы '
                  'латиницы, цифры, дефис и подчёркивание.',
        verbose_name='Идентификатор'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ('title',)

    def __str__(self):
        return self.title


class Post(IsPublishedModel, CreatedAtModel):
    title = models.CharField(
        max_length=settings.MAX_STRING_LENGTH,
        verbose_name='Заголовок'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        help_text='Если установить дату и время в будущем — можно делать '
                  'отложенные публикации.',
        verbose_name='Дата и время публикации'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория'
    )
    image = models.ImageField(
        verbose_name='Изображение у публикации',
        blank=True
    )

    class Meta:
        default_related_name = 'posts'
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date', )

    def __str__(self):
        return self.title


class Comment(CreatedAtModel):
    text = models.TextField(
        verbose_name='Комментарий',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
        ordering = ('created_at',)

    def __str__(self):
        return f'Комментарий пользователя {self.author}'
