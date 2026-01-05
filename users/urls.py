from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig
from users.views import PaymentViewSet, UserViewSet

app_name = UsersConfig.name
# Создание роутера
router = DefaultRouter()

# Регистрация ViewSet для платежей
router.register("payments", PaymentViewSet, basename="payments")

# Регистрация ViewSet
router.register("", UserViewSet, basename="users")

urlpatterns = router.urls
