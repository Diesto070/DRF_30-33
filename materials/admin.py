from django.contrib import admin

from .models import Course, Lesson, Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Настройки отображения модели Course в админке"""
    list_display = ('id', 'name', 'owner', 'description')  # Что показывать в списке


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Настройки отображения модели Lesson в админке"""
    list_display = ('id', 'name', 'course', 'owner', 'video_url')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Настройки отображения модели Subscription в админке"""
    list_display = ('id', 'user', 'course', 'is_active', 'created_at')
# from django.contrib import admin

# Register your models here.
