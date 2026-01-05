from rest_framework.pagination import PageNumberPagination


class CourseLessonPagination(PageNumberPagination):
    """Пагинатор для постраничного вывода списка курсов и уроков."""
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10
