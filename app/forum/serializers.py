from rest_framework import serializers

from core.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for Question model"""

    class Meta:
        model = Question
        fields = ('id', 'name', 'user', 'created_at')
        read_only_fields = ('id', )
