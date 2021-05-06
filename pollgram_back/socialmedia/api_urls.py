from django.urls import path
from .views import user, follow_relationship

urlpatterns = [
    path('user/<int:pk>/', user.UserAPIView.as_view(), name='user_api'),
    path('user/<int:pk>/follow/', follow_relationship.FollowAPIView.as_view(), name='follow-api'),
    path('user/<int:pk>/followings/', follow_relationship.FollowingsAPIView.as_view(), name='followings-api'),
    path('user/<int:pk>/followers/', follow_relationship.FollowersAPIView.as_view(), name='followers-api'),
    path('user/avatar/<int:pk>/', user.UserAvatarAPIView.as_view(), name='avatar_api'),
    path('user/cover/<int:pk>/', user.UserCoverAPIView.as_view(), name='cover_api'),
]