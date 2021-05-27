from django.urls import path
from .views import *

app_name = 'poll'
urlpatterns = [
    path('<int:pk>/', PollRetrieveDestroyAPIView.as_view(), name='poll_retrieve_destroy'),
    path('', PollCreateAPIView.as_view(), name='poll_create'),
    path('<int:poll_pk>/vote/', VoteAPIView.as_view(), name='vote'),
    path('<int:poll_pk>/choice/<int:order>/voters/', VotersListAPIView.as_view(), name='voters'),
    path('image/', ImageCreateAPIView.as_view(), name='image'),
    path('file/', FileCreateAPIView.as_view(), name='file'),
    path('categories/', CategoryListAPIView.as_view(), name='categories'),
    path('category/<int:cat_pk>/polls/', CategoryPollsListAPIView.as_view(), name='category_polls')
]

