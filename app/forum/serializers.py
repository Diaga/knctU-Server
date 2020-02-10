from rest_framework import serializers

from core.models import Question, Answer, Comment, Reply
from user.serializers import UserSerializer


class ReplySerializer(serializers.ModelSerializer):
    """Serializer for Reply model"""

    user = UserSerializer(read_only=True)

    class Meta:
        model = Reply
        fields = ('id', 'text', 'user', 'created_at')
        read_only_fields = ('id',)


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model"""

    replies = ReplySerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'created_at', 'user', 'replies')
        read_only_fields = ('id',)


class AnswerSerializer(serializers.ModelSerializer):
    """Serializer for Answer model"""

    comments = CommentSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    comments_count = serializers.SerializerMethodField('get_comments_count')

    def get_comments_count(self, obj):
        """Return total number of comments"""
        comments_queryset = obj.comments.all()
        replies_queryset = Reply.objects.filter(
            comment__in=comments_queryset
        ).all()
        return comments_queryset.count() + replies_queryset.count()

    class Meta:
        model = Answer
        fields = ('id', 'text', 'user', 'comments', 'created_at', 'comments_count')
        read_only_fields = ('id', 'comments_count')


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for Question model"""

    answers = AnswerSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'user', 'answers', 'created_at')
        read_only_fields = ('id', )
