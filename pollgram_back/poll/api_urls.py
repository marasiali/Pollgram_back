from django.urls import path
from .views import *

app_name = 'poll'
urlpatterns = [
    path('<int:pk>/', PollRetrieveDestroyAPIView.as_view()),
    path('', PollCreateAPIView.as_view()),
    path('vote/<int:poll_pk>/', VoteAPIView.as_view()),
    path('image/', ImageCreateAPIView.as_view(), name='image'),
    path('file/', FileCreateAPIView.as_view(), name='file')
]

