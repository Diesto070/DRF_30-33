from typing import Type

from rest_framework import serializers, status
from rest_framework.generics import (CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView,
                                     get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.paginators import CourseLessonPagination
from materials.serializers import CourseDetailSerializer, CourseSerializer, LessonSerializer, SubscriptionSerializer
from users.permissions import IsModer, IsOwner


class CourseViewSet(ModelViewSet):
    """ViewSet для выполнения всех CRUD операций с курсами."""
    queryset = Course.objects.all()
    pagination_class = CourseLessonPagination

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
            self.permission_classes = [IsAuthenticated, IsOwner]
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
    pagination_class = CourseLessonPagination


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


class SubscriptionAPIView(APIView):
    """API View для управления подписками на курсы."""
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """Подписывает пользователя на курс."""
        user = request.user

        # Получаем id курса из request.data
        course_id = request.data.get('course_id')
        if not course_id:
            return Response(
                {"error": "course_id обязателен"},
                status=status.HTTP_400_BAD_REQUEST
            )

            # Получаем объект курса из базы
        course_item = get_object_or_404(Course, id=course_id)

        # Получаем объекты подписок по текущему пользователю и курсу
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'

        # Возвращаем ответ в API
        return Response({"message": message})
