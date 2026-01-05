from rest_framework.serializers import ValidationError


class URLValidator:
    """Валидатор для проверки, что URL ведёт на YouTube."""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url = value.get(self.field)
        if url and not url.startswith("https://www.youtube.com"):
            raise ValidationError("Ссылка должна вести на youtube.com")
