from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, serializers
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from users.models import Payments, User
from users.serializers import (PaymentsSerializer, UserHistoryPaymentsSerializer, UserRegistrationSerializer,
                               UserSerializer)
from users.services import create_stripe_price, create_stripe_product, create_stripe_sessions


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


class PaymentsCreateAPIView(CreateAPIView):

    """ API View для создания платежей через Stripe.

    Этот View обрабатывает создание платежей для курсов или уроков."""
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    def perform_create(self, serializer):
        """Создает платеж и сессию оплаты в Stripe.

        Логика работы:
        1. Сохраняет платеж в базе данных с привязкой к текущему пользователю
        2. Определяет оплачиваемый курс или урок
        3. Создает продукт в Stripe на основе названия курса/урока
        4. Создает цену в Stripe в рублях (конвертирует рубли в копейки)
        5. Создает сессию оплаты в Stripe и получает ссылку для оплаты
        6. Сохраняет ID сессии и ссылку в объекте платежа"""

        # Создаем платеж в базе
        payment = serializer.save(user=self.request.user)

        # Получаем курс или урок для оплаты
        course = payment.course_paid
        lesson = payment.lesson_paid
        # Определяем, что оплачивается: курс или урок
        if course:
            product_name = course.name
        elif lesson:
            product_name = lesson.name
        else:
            # Если ни курс, ни урок не указаны - выбрасываем ошибку
            raise serializers.ValidationError(
                "Необходимо указать курс или урок для оплаты"
            )
        # Создаем продукт в Stripe
        product = create_stripe_product(product_name)

        # Создаем цену в Stripe
        price = create_stripe_price(payment.amount, product.id)
        # Создаем сессию оплаты
        session_id, payment_link = create_stripe_sessions(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


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
