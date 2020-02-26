from core.handlers import GenericHandler

from .serializers import QuestionSerializer


class QuestionHandler(GenericHandler):
    """Handle Question model subscription"""

    def is_valid(self):
        """Check if consumer is valid"""
        return self.user.is_authenticated

    def get_group_name(self):
        """Return group name"""
        return self.data.get('id', None)

    @staticmethod
    def update_question(info, instance, user=None):
        return QuestionHandler.update(info, QuestionSerializer(instance, 'context': {'user': None}),
                                      [instance.id])
