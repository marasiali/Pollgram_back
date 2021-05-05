from django.urls import path, include
from .views import user

urlpatterns = [
    path('user/<int:pk>/', user.UserAPIView.as_view(), name='user_api'),
    path('user/avatar/<int:pk>/', user.UserAvatarAPIView.as_view(), name='avatar_api'),
    path('user/cover/<int:pk>/', user.UserCoverAPIView.as_view(), name='cover_api'),

    path('user/', user.UserListAPIView.as_view(), name='user_list_api'),
]