from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import PaymentViewSet, UserRegistration, UserViewSet

app_name = UsersConfig.name
# Создание роутера
router = DefaultRouter()

# Регистрация ViewSet для платежей
router.register("payments", PaymentViewSet, basename="payments")

# Регистрация ViewSet
router.register("", UserViewSet, basename="users")

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
] + router.urls
