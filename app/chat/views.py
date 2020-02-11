from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import ChatRoom
from . import serializers


class ChatRoomViewSet(viewsets.GenericViewSet):
    """View set for ChatRoom model"""

    authentication_classes = [TokenAuthentication, ]

    permission_classes = [IsAuthenticated, ]

    queryset = ChatRoom.objects.all()

    serializer_class = serializers.ChatRoomSerializer

    def get_queryset(self):
        """Enforce scope"""
        return self.request.user.chat_rooms.all()

    def view_chat_room(self, request, *args, **kwargs):
        """Return scoped chat rooms"""
        serializer = self.get_serializer(
            self.get_queryset(), many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
