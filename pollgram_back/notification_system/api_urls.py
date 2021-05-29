from django.urls import path
from .views import (
    NotificationAllListAPIView,
    NotificationUnreadListAPIView,
    NotificationAllCountAPIView,
    NotificationUnreadCountAPIView,
    NotificationMarkAsReadAPIView,
    NotificationMarkAsUnreadAPIView,
    NotificationMarkAllAsReadAPIView,
)

urlpatterns = [
    path('mark-all-as-read/', NotificationMarkAllAsReadAPIView.as_view(), name='mark_all_as_read'),
    path('mark-as-read/<slug:slug>/', NotificationMarkAsReadAPIView.as_view(), name='mark_as_read'),
    path('mark-as-unread/<slug:slug>/', NotificationMarkAsUnreadAPIView.as_view(), name='mark_as_unread'),
    path('', NotificationAllListAPIView.as_view(), name='all_notifications'),
    path('count/', NotificationAllCountAPIView.as_view(), name='all_notifications_count'),
    path('unread/', NotificationUnreadListAPIView.as_view(), name='unread_notifications'),
    path('unread/count/', NotificationUnreadCountAPIView.as_view(), name='unread_notifications_count'),
]