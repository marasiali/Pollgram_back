from django.urls import path
from .views.follow_relationship import FollowAPIView, FollowingsAPIView, FollowersAPIView, \
    FollowRequestStatusHandlerAPIView, FollowRequestListAPIView
from .views.user import UserAPIView, UserAvatarAPIView, UserCoverAPIView, UserTimelineListAPIView, PollListAPIView, \
    UserListAPIView, BlockUserAPIView, BlockedUsersListAPIView

urlpatterns = [
    path('user/', UserListAPIView.as_view(), name='user_list_api'),
    path('user/<int:pk>/', UserAPIView.as_view(), name='user_api'),
    path('user/<int:pk>/block/', BlockUserAPIView.as_view(), name='block_api'),
    path('user/blocklist/', BlockedUsersListAPIView.as_view(), name='blocklist_api'),
    path('user/avatar/', UserAvatarAPIView.as_view(), name='avatar_api'),
    path('user/cover/', UserCoverAPIView.as_view(), name='cover_api'),
    path('user/timeline/', UserTimelineListAPIView.as_view(), name='timeline_api'),
    path('user/<int:pk>/polls/', PollListAPIView.as_view(), name='user_polls_api'),

    path('user/<int:pk>/follow/', FollowAPIView.as_view(), name='follow-api'),
    path('user/<int:pk>/followings/', FollowingsAPIView.as_view(), name='followings-api'),
    path('user/<int:pk>/followers/', FollowersAPIView.as_view(), name='followers-api'),
    path('user/<int:user_pk>/follow-request-status/', FollowRequestStatusHandlerAPIView.as_view(),
         name='follow_request_status'),
    path('user/follow-request/', FollowRequestListAPIView.as_view(), name='follow_request_list'),
]
