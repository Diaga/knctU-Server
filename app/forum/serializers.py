from rest_framework import serializers

from core.models import Question, Answer, Comment, Reply, Tag, InfoUser
from user.serializers import UserSerializer, TagSerializer


class InfoUserSerializer(serializers.ModelSerializer):
    """Serializer for Info User"""

    class Meta:
        model = InfoUser
        fields = ('id', 'name', 'has_upvoted', 'has_viewed', 'has_shared',
                  'question', 'answer', 'comment', 'reply')
        read_only_fields = ('id', )


class ReplySerializer(serializers.ModelSerializer):
    """Serializer for Reply model"""

    user = UserSerializer(read_only=True)

    class Meta:
        model = Reply
        fields = ('id', 'text', 'user', 'created_at')
        read_only_fields = ('id', 'created_at')

    def create(self, validated_data):
        """Add authenticated user"""
        validated_data.update({'user': self.context['user'].user})
        return super(ReplySerializer, self).create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model"""

    replies = ReplySerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'created_at', 'user', 'replies',
                  'created_at')
        read_only_fields = ('id',)

    def create(self, validated_data):
        """Add authenticated user"""
        validated_data.update({'user': self.context['user'].user})
        return super(CommentSerializer, self).create(validated_data)


class AnswerSerializer(serializers.ModelSerializer):
    """Serializer for Answer model"""

    comments = CommentSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    comments_count = serializers.SerializerMethodField('get_comments_count')

    info_user = serializers.SerializerMethodField('get_info_user')
    upvote_count = serializers.SerializerMethodField('get_upvote_count')
    view_count = serializers.SerializerMethodField('get_view_count')

    def get_info_user(self, obj):
        """Return current info user"""
        user = None
        request = self.context.get('request', None)
        if request is None:
            request = self.context.get('user', None)
            if request is not None:
                user = request
            else:
                return None
        else:
            user = request.user
        query = obj.info_user_set.filter(
            user=user
        )
        if query.exists():
            return InfoUserSerializer(query.first()).data
        return InfoUserSerializer(
            InfoUser.objects.create(
                name='answer', user=user, answer=obj,
                has_viewed=True
            )
        ).data

    def get_upvote_count(self, obj):
        """Return upvote count"""
        return obj.info_user_set.filter(
            has_upvoted=True
        ).count()

    def get_view_count(self, obj):
        """Return view count"""
        return obj.info_user_set.filter(
            has_viewed=True
        ).count()

    def get_comments_count(self, obj):
        """Return total number of comments"""
        comments_queryset = obj.comments.all()
        replies_queryset = Reply.objects.filter(
            comment__in=comments_queryset
        ).all()
        return comments_queryset.count() + replies_queryset.count()

    class Meta:
        model = Answer
        fields = ('id', 'text', 'user', 'comments', 'created_at',
                  'comments_count', 'info_user', 'upvote_count', 'view_count')
        read_only_fields = ('id', 'comments_count', 'created_at')

    def create(self, validated_data):
        """Add authenticated user"""
        validated_data.update({'user': self.context['user'].user})
        return super(AnswerSerializer, self).create(validated_data)


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for Question model"""

    answers = AnswerSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    tags = TagSerializer(many=True)

    info_user = serializers.SerializerMethodField('get_info_user')
    upvote_count = serializers.SerializerMethodField('get_upvote_count')
    view_count = serializers.SerializerMethodField('get_view_count')

    def get_info_user(self, obj):
        """Return current info user"""
        user = None
        request = self.context.get('request', None)
        if request is None:
            request = self.context.get('user', None)
            if request is not None:
                user = request
            else:
                return None
        else:
            user = request.user
        query = obj.info_user_set.filter(
            user=user
        )
        if query.exists():
            return InfoUserSerializer(query.first()).data
        return InfoUserSerializer(
            InfoUser.objects.create(
                name='question', user=user, question=obj,
                has_viewed=True
            )
        ).data

    def get_upvote_count(self, obj):
        """Return upvote count"""
        return obj.info_user_set.filter(
            has_upvoted=True
        ).count()

    def get_view_count(self, obj):
        """Return view count"""
        return obj.info_user_set.filter(
            has_viewed=True
        ).count()

    class Meta:
        model = Question
        fields = ('id', 'text', 'user', 'answers', 'created_at', 'tags',
                  'info_user', 'upvote_count', 'view_count')
        read_only_fields = ('id', 'created_at')

    def create(self, validated_data):
        """Add authenticated user"""
        validated_data.update({'user': self.context['user'].user})
        return super(QuestionSerializer, self).create(validated_data)
