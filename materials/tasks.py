from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from users.models import User


@shared_task
def send_email_about_update_the_course_materials(email, subject, message):
    """Асинхронная рассылка писем всем подписчикам курса об обновлении."""
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )


@shared_task
def block_inactive_users():
    """Блокировка пользователей, которые не заходили более месяца."""
    # Рассчитываем дату, которая была 30 дней назад
    month_ago = timezone.now() - timedelta(days=30)

    # Находим пользователей, которые не заходили более месяца и еще активны
    inactive_users = User.objects.filter(last_login__lt=month_ago, is_active=True)
    # Блокируем пользователей
    inactive_users.update(is_active=False)
