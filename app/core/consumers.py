from channels.generic.websocket import JsonWebsocketConsumer

from chat.handlers import ChatRoomHandler
from forum.handlers import QuestionHandler

from asgiref.sync import async_to_sync


class SubscribeConsumer(JsonWebsocketConsumer):
    """Generic Consumer that allows subscribing to any object"""

    def connect(self):
        """Always accept connections"""
        self.accept()
        user = self.scope.get('user', None)
        if user.is_authenticated:
            group_name = str(user.id)
            self.groups.append(group_name)
            async_to_sync(self.channel_layer.group_add)(
                group_name, self.channel_name
            )

    def notify(self, event):
        """Pass of handling events to handlers"""
        self.send_json(event["content"])

    def receive_json(self, content, **kwargs):
        """Handle data from client"""
        handler = self.get_handler(content)
        if handler is None:
            return {'error': 'Consumer handler not found!'}
        if not handler.is_valid():
            return {'error': 'Permission denied!'}

        group_name = str(handler.get_group_name())
        self.groups.append(group_name)

        async_to_sync(self.channel_layer.group_add)(
            group_name,
            self.channel_name,
        )

    def get_handler(self, data):
        """Enforce scope"""
        model = data.get('model', None)
        if model == 'forum.question':
            return QuestionHandler(self.scope.get('user', None), data)
        elif model == 'chat.chat_room':
            handler = ChatRoomHandler(self.scope.get('user', None), data)
            if handler.is_valid():
                handler.handle_db()
            return handler
        return None

