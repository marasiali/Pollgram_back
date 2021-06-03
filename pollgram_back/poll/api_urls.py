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
    path('category/', CategoryListAPIView.as_view(), name='categories'),
    path('category/<int:cat_pk>/', CategoryPollsListAPIView.as_view(), name='category_polls'),

    path('<int:poll_pk>/comment/', CommentListCreateAPIView.as_view(), name='comment_list_create'),
    path('<int:poll_pk>/comment/<int:comment_pk>/', CommentRetrieveDestroyAPIView.as_view(), name='comment_retrieve_destroy'),

    path('<int:poll_pk>/comment/<int:comment_pk>/reply/', ReplyListAPIView.as_view(), name='comment_replies'),

    path('<int:poll_pk>/comment/<int:comment_pk>/like/', LikeAPIView.as_view(), name='like'),
    path('<int:poll_pk>/comment/<int:comment_pk>/dislike/', DislikeAPIView.as_view(), name='dislike'),

    path('<int:poll_pk>/chart/circle/', CircularChartAPIView.as_view(), name='circle_chart'),

]

