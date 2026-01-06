from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from users.models import Payments, User
from users.serializers import (PaymentsSerializer, UserHistoryPaymentsSerializer, UserRegistrationSerializer,
                               UserSerializer)


class PaymentViewSet(ModelViewSet):
    """ViewSet для платежей с фильтрацией:
    1. Сортировка по дате оплаты (ordering)
    2. Фильтрация по курсу или уроку
    3. Фильтрация по способу оплаты"""
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['course_paid', 'lesson_paid', 'method_payment']
    ordering_fields = ['date_payment']
    # Сортировка по умолчанию (новые первыми)
    ordering = ['-date_payment']


class UserViewSet(ModelViewSet):
    """ViewSet для пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRegistration(CreateAPIView):
    """APIView для создания пользователя"""
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)    # разрешает доступ всем пользователям, включая анонимных.

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserHistoryPaymentsViewSet(ModelViewSet):
    """ViewSet для истории платежей пользователя"""

    serializer_class = UserHistoryPaymentsSerializer

    def get_queryset(self) -> QuerySet[User]:
        # Предзагрузка платежей пользователя для оптимизации запросов
        return User.objects.prefetch_related('payments_set')
