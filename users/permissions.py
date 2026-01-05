from rest_framework import permissions, request, views


class IsModer(permissions.BasePermission):
    """Permission для проверки принадлежности пользователя к группе модераторов.

    Проверяет, состоит ли аутентифицированный пользователь в группе с названием
    "moderators". Если пользователь не аутентифицирован или не состоит в указанной
    группе, доступ запрещается."""
    def has_permission(self, request: request.Request, view: views.APIView) -> bool:
        """Проверяет право доступа пользователя к представлению."""
        return request.user.is_authenticated and request.user.groups.filter(name="moderators").exists()


class IsOwner(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем."""
    def has_object_permission(self, request: request.Request, view: views.APIView, obj) -> bool:

        if obj.owner == request.user:
            """Проверяет право доступа к конкретному объекту."""
            return True
        return False
