from django.db import transaction

from core.handlers import GenericHandler
from core.models import ChatRoom, Message, MessageUser

from .serializers import ChatRoomSerializer, MessageSerializer, \
    MessageUserSerializer


class ChatRoomHandler(GenericHandler):
    """Handler ChatRoom for all chat functionality"""

    info = None

    def __init__(self, user, data):
        self.info = data.pop('info', None)
        super(ChatRoomHandler, self).__init__(user, data)

    def handle_db(self):
        """Handle db transactions"""
        with transaction.atomic():
            if self.info == 'CREATE_MESSAGE':
                message = None
                self.data['payload'].update({'user_id': self.user.id,
                                             'chat_room': self.data['id']})
                serializer = MessageSerializer(data=self.data['payload'])
                if serializer.is_valid(raise_exception=True):
                    message = serializer.save()
            elif self.info == 'UPDATE_MESSAGE_USER':
                message_user = MessageUser.objects.filter(
                    id=self.data['payload'].get('id', None)
                ).first()
                serializer = MessageUserSerializer(message_user,
                                                   data=self.data['payload'])
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
            elif self.info == 'CREATE_CHATROOM':
                chat_room = None
                users = self.data['payload'].pop('users', [])
                serializer = ChatRoomSerializer(data=self.data['payload'])
                if serializer.is_valid(raise_exception=True):
                    chat_room = serializer.save()
                chat_room.users.add(*users)
                self.data.update({'id': str(chat_room.id)})

    def is_valid(self):
        """Check if consumer is valid"""
        if self.info == 'CREATE_CHATROOM':
            return self.user.is_authenticated
        return self.user in ChatRoom.objects.filter(
            id=self.data.get('id')
        ).first().users.all()

    def get_group_name(self):
        """Return group name"""
        return self.user.id

    @staticmethod
    def update_chat_room(info, instance):
        return ChatRoomHandler.update(info, ChatRoomSerializer(instance),
                                      instance.users.values_list('id',
                                                                 flat=True))
