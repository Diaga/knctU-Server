from abc import ABC, abstractmethod
from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync


class GenericHandler(ABC):
    """Handle Question model subscription"""

    user = None
    data = None

    def __init__(self, user, data):
        self.user = user
        self.data = data

    @abstractmethod
    def is_valid(self):
        """Check if consumer is valid"""
        pass

    @staticmethod
    def update(info, serializer, channel_ids):
        """Send change event to all subscribed clients"""
        channel_layer = get_channel_layer()

        content = {
            'type': info,
            'payload': serializer.data
        }

        wrapper = {
            'type': 'notify',
            'content': content
        }

        for channel_id in channel_ids:
            async_to_sync(channel_layer.group_send)(str(channel_id), wrapper)
