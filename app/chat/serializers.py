from rest_framework import serializers

from core.models import ChatRoom, Message, MessageUser, User
from user.serializers import UserSerializer


class MessageUserSerializer(serializers.ModelSerializer):
    """Serializer for MessageUser model"""

    user = UserSerializer(required=False)

    class Meta:
        model = MessageUser
        fields = ('id', 'is_read', 'user')
        read_only_fields = ('id', 'user')


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model"""

    user_id = serializers.PrimaryKeyRelatedField(
        source='user', write_only=True, queryset=User.objects.all())
    message_users = MessageUserSerializer(many=True, required=False)

    user = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'user', 'text', 'message_users', 'user_id',
                  'chat_room', 'created_at')
        read_only_fields = ('id', 'created_at', 'message_users')
        extra_kwargs = {
            'chat_room': {'write_only': True}
        }


class ChatRoomSerializer(serializers.ModelSerializer):
    """Serializer for ChatRoom model"""

    messages = MessageSerializer(many=True, read_only=True)
    users = UserSerializer(many=True, required=False)

    class Meta:
        model = ChatRoom
        fields = ('id', 'name', 'users', 'messages')
        read_only_fields = ('id', 'created_at', 'users')
