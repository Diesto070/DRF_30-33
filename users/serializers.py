from rest_framework.serializers import ModelSerializer

from users.models import Payments, User


class PaymentsSerializer(ModelSerializer):
    """Сериализатор для модели Платежи."""

    class Meta:
        """Метаданные сериализатора платежи."""
        model = Payments
        fields = "__all__"


class UserSerializer(ModelSerializer):
    """Сериализатор для модели Пользователь."""
    payments_set = PaymentsSerializer(many=True, read_only=True)

    class Meta:
        """Метаданные сериализатора пользователь."""
        model = User
        fields = ("id", "email", "phone", "city", "avatar", "payments_set")

    def update(self, instance, validated_data):
        """Кастомная логика обновления в сериализаторе"""
        return super().update(instance, validated_data)


class UserHistoryPaymentsSerializer(ModelSerializer):
    """Сериализатор для модели История платежей."""
    payments_set = PaymentsSerializer(many=True, read_only=True)

    class Meta:
        """Метаданные сериализатора История платежей."""
        model = User
        fields = ("id", "email", "phone", "city", "payments_set")
