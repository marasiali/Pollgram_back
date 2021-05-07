from django.urls import path
from .views import *

app_name = 'poll'
urlpatterns = [
    path('<int:pk>/', PollRetrieveDestroyAPIView.as_view()),
    path('', PollCreateAPIView.as_view()),
    path('vote/<int:pk>/', VoteCreateAPIView.as_view())
]

