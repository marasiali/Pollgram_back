from rest_framework.pagination import PageNumberPagination


class PollPagination(PageNumberPagination):
    page_size = 10
