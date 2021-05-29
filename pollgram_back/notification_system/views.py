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

class NotificationAllListAPIView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = NotificationPagination
    def get_queryset(self):
        return self.request.user.notifications.all()


class NotificationUnreadListAPIView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = NotificationPagination
    def get_queryset(self):
        return self.request.user.notifications.unread()


class NotificationAllCountAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @method_decorator(never_cache)
    def get(self, request):
        return Response({
            "count": self.request.user.notifications.all().count(),
        })


class NotificationUnreadCountAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @method_decorator(never_cache)
    def get(self, request):
        return Response({
            "count": self.request.user.notifications.unread().count(),
        })


class NotificationMarkAsReadAPIView(APIView):
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
    permission_classes = [IsAuthenticated]
    def post(self, request):
        request.user.notifications.mark_all_as_read()
        return Response({
            "msg": "ok",
        })