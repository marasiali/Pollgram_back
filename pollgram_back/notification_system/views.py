from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from notifications.models import Notification
from notifications.utils import slug2id
from .serializers import NotificationSerializer
from .paginations import NotificationPagination
from drf_spectacular.utils import extend_schema


class NotificationAllListAPIView(ListAPIView):
    """
    Get list of all notifications

    In the response:

        - slug          ->  Notification id
        - actor         ->  The user who performed the activity.
        - action        ->  Type of this notification    
        - action_object ->  The object linked to the action itself.        
        - target        ->  The object to which the activity was performed.    
        - unread        ->  Has the notification been read? (NOTE: You must mark notification as read manually.)
        - timestamp     ->  notification time    

    Based on "action" may be "action_object" or "target" or both of them be null.

    Meaning of "actor", "action_object" and "target" explained in the examples for each
    type of notification.
    
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = NotificationPagination
    def get_queryset(self):
        return self.request.user.notifications.all()


class NotificationUnreadListAPIView(ListAPIView):
    """
    Get list of unread notifications.

    In the response:

        - slug          ->  Notification id
        - actor         ->  The user who performed the activity.
        - action        ->  Type of this notification    
        - action_object ->  The object linked to the action itself.        
        - target        ->  The object to which the activity was performed.    
        - unread        ->  Has the notification been read? (NOTE: You must mark notification as read manually.)
        - timestamp     ->  notification time    

    Based on "action" may be "action_object" or "target" or both of them be null.

    Meaning of "actor", "action_object" and "target" explained in the examples for each
    type of notification.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = NotificationPagination
    def get_queryset(self):
        return self.request.user.notifications.unread()


class NotificationAllCountAPIView(APIView):
    """
    Get all notifications count.
    """
    permission_classes = [IsAuthenticated]
    @method_decorator(never_cache)
    def get(self, request):
        return Response({
            "count": self.request.user.notifications.all().count(),
        })


class NotificationUnreadCountAPIView(APIView):
    """
    Get unread notifications count.
    """
    permission_classes = [IsAuthenticated]
    @method_decorator(never_cache)
    def get(self, request):
        return Response({
            "count": self.request.user.notifications.unread().count(),
        })


class NotificationMarkAsReadAPIView(APIView):
    """
    Mark a notification as read.
    """
    permission_classes = [IsAuthenticated]
    def post(self, request, slug):
        notification_id = slug2id(slug)
        notification = get_object_or_404(
            Notification, recipient=request.user, id=notification_id)
        notification.mark_as_read()
        return Response({
            "msg": "ok",
        })


class NotificationMarkAsUnreadAPIView(APIView):
    """
    Mark a notification as unread.
    """
    permission_classes = [IsAuthenticated]
    def post(self, request, slug):
        notification_id = slug2id(slug)
        notification = get_object_or_404(
            Notification, recipient=request.user, id=notification_id)
        notification.mark_as_unread()
        return Response({
            "msg": "ok",
        })


class NotificationMarkAllAsReadAPIView(APIView):
    """
    Mark all notifications as read.
    """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        request.user.notifications.mark_all_as_read()
        return Response({
            "msg": "ok",
        })