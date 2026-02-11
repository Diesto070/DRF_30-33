from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя с email для авторизации"""

    username = None
    email = models.EmailField(unique=True, verbose_name="Почта", help_text="Укажите почту")

    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите номер телефона",
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payments(models.Model):
    """Модель для хранения информации о платежах."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Выберите пользователя",
    )
    date_payment = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата платежа",
    )
    course_paid = models.ForeignKey(
        'materials.Course',
        on_delete=models.CASCADE,
        verbose_name="Оплаченный курс",
        null=True,
        blank=True,
    )
    lesson_paid = models.ForeignKey(
        'materials.Lesson',
        on_delete=models.CASCADE,
        verbose_name="Оплаченный урок",
        null=True,
        blank=True,
    )
    amount = models.PositiveIntegerField(
        verbose_name="Сумма оплаты",
        help_text="Укажите сумму оплаты",
    )
    method_payment = models.CharField(
        max_length=10,
        choices=[("cash", "Наличные"), ("transfer", "Перевод на счет"), ("stripe", "Stripe онлайн-оплата")],
        verbose_name="Способ оплаты",
        help_text="Выберите способ оплаты",
    )
    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Id сессии",
        help_text="Укажите id сессии",
    )
    link = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату",
        help_text="Укажите ссылку на оплату",
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["-date_payment"]  # новые платежи первыми

    def __str__(self):
        return f"{self.user} - {self.amount}"
