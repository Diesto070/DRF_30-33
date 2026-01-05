from django.db import models

from config import settings


class Course(models.Model):
    """Модель курса"""

    name = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Укажите название курса",
    )
    picture = models.ImageField(
        upload_to="materials/courses/",
        verbose_name="Превью курса",
        help_text="Загрузите фото курса",
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name="Описание курса",
        help_text="Укажите описание курса",
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец курса",
        help_text="Укажите владельца курса",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    """Модель урока в рамках курса"""
    name = models.CharField(
        max_length=100,
        verbose_name="Название урока",
        help_text="Укажите название урока",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        help_text="Выберите курс",
    )
    description = models.TextField(
        verbose_name="Описание урока",
        help_text="Укажите описание урока",
        blank=True,
        null=True,
    )
    picture = models.ImageField(
        upload_to="materials/lessons/",
        verbose_name="Превью урока",
        help_text="Загрузите превью урока",
        blank=True,
        null=True,
    )
    video_url = models.URLField(
        verbose_name="Ссылка на видео урока",
        help_text="Введите ссылку на видео урока",
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
        help_text="Укажите владельца",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    """Модель подписки на курс"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Укажите пользователя",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        help_text="Укажите курс"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f'Подписка пользователя {self.user} на курс {self.course}'
