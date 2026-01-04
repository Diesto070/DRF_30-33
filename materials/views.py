from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(ModelViewSet):
    """ViewSet для выполнения всех CRUD операций с курсами."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonCreateApiView(CreateAPIView):
    """API View для создания нового урока.
    Обрабатывает POST запросы для создания уроков."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonListApiView(ListAPIView):
    """API View для получения списка всех уроков.
    Обрабатывает GET запросы для получения списка уроков."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveApiView(RetrieveAPIView):
    """API View для получения детальной информации об уроке.
    Обрабатывает GET запросы для получения конкретного урока по ID."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateApiView(UpdateAPIView):
    """API View для обновления существующего урока.
    Обрабатывает PUT и PATCH запросы для обновления урока.
    PUT - полное обновление, PATCH - частичное обновление."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyApiView(DestroyAPIView):
    """API View для удаления урока.
    Обрабатывает DELETE запросы для удаления урока по ID."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
