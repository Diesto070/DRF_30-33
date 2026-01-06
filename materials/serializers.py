from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson, Subscription
from materials.validators import URLValidator


class LessonSerializer(ModelSerializer):
    """Сериализатор для модели Lesson (урока).
    Преобразует объекты уроков в JSON и обратно для API.
    Включает все поля модели и информацию о курсе."""
    class Meta:
        """Метаданные сериализатора урока."""
        model = Lesson
        fields = "__all__"
        validators = [URLValidator(field="video_url")]


class CourseSerializer(ModelSerializer):
    """Сериализатор для модели Course (курс).
    Преобразует объекты курсов в JSON и обратно для API.
    Включает все поля модели, включая связанные уроки."""

    # получаем признак подписки пользователя на курс
    is_subscribed = SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return Subscription.objects.filter(user=user, course=obj).exists()

    class Meta:
        """Метаданные сериализатора курса."""
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    """Сериализатор для детального представления курса.

     Предоставляет расширенную информацию о курсе, включая:
    - Основные данные курса
    - Полную информацию по всем урокам курса
    - Количество уроков в курсе

    Оба поля (lessons и count_lessons) выводятся одновременно в одном ответе.
    Информация об уроках предоставляется через связанный сериализатор LessonSerializer."""

    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    count_lessons = SerializerMethodField()

    # получаем признак подписки пользователя на курс
    is_subscribed = SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return Subscription.objects.filter(user=user, course=obj).exists()

    def get_count_lessons(self, course):
        """Возвращает количество уроков в курсе."""
        return course.lesson_set.count()

    class Meta:
        """Метаданные сериализатора курса."""
        model = Course
        fields = ("name", "lessons", "count_lessons", 'is_subscribed')


class SubscriptionSerializer(ModelSerializer):
    """Сериализатор для модели подписки на курс.

    Преобразует объекты подписки на курс в JSON и обратно для API."""

    class Meta:
        model = Subscription
        fields = "__all__"
        read_only_fields = ("user", "created_at")
