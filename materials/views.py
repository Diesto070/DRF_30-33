from typing import Type

from rest_framework import serializers
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.serializers import CourseDetailSerializer, CourseSerializer, LessonSerializer
from users.permissions import IsModer, IsOwner


class CourseViewSet(ModelViewSet):
    """ViewSet для выполнения всех CRUD операций с курсами."""
    queryset = Course.objects.all()

    def get_serializer_class(self) -> Type[serializers.Serializer]:
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self) -> None:
        """Определяем permissions в зависимости от действия."""
        if self.action == "create":
            # Создавать курсы могут только аутентифицированные пользователи НЕ модераторы
            self.permission_classes = [IsAuthenticated, ~IsModer]
        elif self.action == "list":
            # Просматривать курсы могут только владельцы или модераторы
            self.permission_classes = [IsAuthenticated, IsOwner | IsModer]
        elif self.action in ["update", "partial_update", "retrieve"]:
            # Смотреть и редактировать могут владельцы ИЛИ модераторы
            self.permission_classes = [IsAuthenticated, IsOwner | IsModer]
        elif self.action == "destroy":
            # Удалять могут только владельцы И НЕ модераторы
            self.permission_classes = [IsAuthenticated, IsOwner & ~IsModer]
        return super().get_permissions()

    def perform_create(self, serializer: serializers.Serializer) -> None:
        """Автоматически устанавливает текущего пользователя как владельца создаваемого объекта."""
        serializer.save(owner=self.request.user)


class LessonCreateApiView(CreateAPIView):
    """API View для создания нового урока.
    Обрабатывает POST запросы для создания уроков."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer: serializers.Serializer) -> None:
        """Автоматически устанавливает текущего пользователя как владельца создаваемого объекта."""
        serializer.save(owner=self.request.user)


class LessonListApiView(ListAPIView):
    """API View для получения списка всех уроков.
    Обрабатывает GET запросы для получения списка уроков."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModer]


class LessonRetrieveApiView(RetrieveAPIView):
    """API View для получения детальной информации об уроке.
    Обрабатывает GET запросы для получения конкретного урока по ID."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner | IsModer]


class LessonUpdateApiView(UpdateAPIView):
    """API View для обновления существующего урока.
    Обрабатывает PUT и PATCH запросы для обновления урока.
    PUT - полное обновление, PATCH - частичное обновление."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner | IsModer]


class LessonDestroyApiView(DestroyAPIView):
    """API View для удаления урока.
    Обрабатывает DELETE запросы для удаления урока по ID."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]