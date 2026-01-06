from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from materials.validators import URLValidator
from users.models import User


class LessonTestCase(APITestCase):
    """Тесты для CRUD операций с уроками."""
    def setUp(self):
        """Настройка тестовых данных для тестов уроков.
        Создает пользователя, курс и урок для тестирования."""
        self.user = User.objects.create(email="email_test@test.com")
        self.course = Course.objects.create(name="Test-course", owner=self.user)
        self.lesson = Lesson.objects.create(name="Test-lesson", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)
        # Создаем валидатор для тестирования
        self.validator = URLValidator(field="video_url")

    def test_lesson_retrieve(self):
        """Тест получения детальной информации об уроке."""
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), self.lesson.name
        )

    def test_lesson_create(self):
        """Тест создания нового урока."""
        url = reverse("materials:lessons_create")
        data = {
            "name": "Test-lesson2",
            "course": self.course.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(),
            2
        )

    def test_lesson_create_not_valid(self):
        """Тест создания урока с невалидным видео URL."""
        url = reverse("materials:lessons_create")
        data = {
            "name": "Урок с VK видео",
            "description": "Описание",
            "video_url": "https://www.vk.ru/video123",  # Не YouTube!
            "course": self.course.id
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            Lesson.objects.all().count(),
            1
        )

    def test_lesson_create_with_valid_youtube_url(self):
        """Создание урока с валидным YouTube URL."""
        url = reverse("materials:lessons_create")
        data = {
            "name": "Урок с YouTube",
            "description": "Описание урока",
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "course": self.course.id
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.count(),
            2
        )

    def test_lesson_update(self):
        """Тест обновления существующего урока."""
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {
            "name": "Test-lesson2-new"
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), "Test-lesson2-new"
        )

    def test_lesson_delete(self):
        """Тест удаления урока."""
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(),
            0
        )

    def test_lesson_list(self):
        """Тест получения списка уроков с пагинацией."""
        url = reverse("materials:lessons_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.lesson.id,
                    'name': self.lesson.name,
                    'description': None,
                    'picture': None,
                    'video_url': None,
                    'course': self.course.id,
                    'owner': self.user.id
                }
            ]
        }
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data,
            result
        )
        self.assertEqual(
            response.data['results'][0]['name'],
            self.lesson.name
        )


class CourseTestCase(APITestCase):
    """Тесты для CRUD операций с курсами."""
    def setUp(self):
        """Настройка тестовых данных для тестов курсов.
        Создает пользователя, курс и урок для тестирования.
        """
        self.user = User.objects.create(email="email_test@test.com")
        self.course = Course.objects.create(name="Test-course", owner=self.user)
        self.lesson = Lesson.objects.create(name="Test-lesson", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        """Тест получения детальной информации о курсе."""
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), self.course.name
        )

    def test_course_create(self):
        """Тест создания нового курса."""
        url = reverse("materials:course-list")
        data = {
            "name": "Test-course",
            "course": self.course.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            Course.objects.all().count(),
            2
        )

    def test_course_update(self):
        """Тест обновления существующего курса."""
        url = reverse("materials:course-detail", args=(self.course.pk,))
        data = {
            "name": "Test-lesson2-new"
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), "Test-lesson2-new"
        )

    def test_course_delete(self):
        """Тест удаления курса."""
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Course.objects.count(),
            0
        )

    def test_course_list(self):
        """Тест получения списка курсов с пагинацией."""
        url = reverse("materials:course-list")
        response = self.client.get(url)
        data = response.json()

        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.course.id,
                    'is_subscribed': False,
                    'name': self.course.name,
                    'picture': None,
                    'description': None,
                    'owner': self.user.id
                }
            ]
        }
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            data,
            result
        )
        self.assertEqual(
            response.data['results'][0]['name'],
            self.course.name
        )


class SubscriptionTestCase(APITestCase):
    """Тесты для функционала подписок на курсы."""
    def setUp(self):
        """Настройка тестовых данных для тестов подписок.
        Создает пользователя и курс для тестирования подписок."""
        self.user = User.objects.create(email="email_test@test.com")
        self.course = Course.objects.create(name="Test-course", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        """Тест создания подписки на курс."""
        url = reverse("materials:subscriptions")
        data = {
            "course_id": self.course.pk
        }
        # Создаем подписку
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data["message"],
            "подписка добавлена"
        )
        # Проверяем, что подписка создалась в БД
        self.assertEqual(
            Subscription.objects.filter(
                user=self.user,
                course=self.course
            ).count(),
            1)

    def test_subscription_delete(self):
        """Тест удаления подписки (отписки)."""
        url = reverse("materials:subscriptions")
        data = {"course_id": self.course.pk}

        # Сначала создаем подписку
        Subscription.objects.create(user=self.user, course=self.course)
        initial_count = Subscription.objects.count()
        self.assertEqual(initial_count, 1)

        # Удаляем подписку
        response = self.client.post(url, data)
        self.assertEqual(
            response.data["message"],
            "подписка удалена"
        )

        # Проверяем, что подписки нет в БД
        self.assertEqual(
            Subscription.objects.count(),
            0
        )

    def test_subscription_create_without_course_id(self):
        """Тест создания подписки без course_id (должна быть ошибка 400)."""
        url = reverse("materials:subscriptions")
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.data["error"],
            "course_id обязателен"
        )
