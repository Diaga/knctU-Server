from django.contrib.auth import authenticate

from rest_framework import serializers

from core.models import User, Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id', )


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""

    tags = TagSerializer(many=True)

    question_count = serializers.SerializerMethodField('get_question_count')
    answer_count = serializers.SerializerMethodField('get_answer_count')

    def get_question_count(self, obj):
        """Return number of questions asked by user"""
        return obj.questions.count()

    def get_answer_count(self, obj):
        """Return number of answers given by user"""
        return obj.answers.count()

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password', 'title', 'tags',
                  'question_count', 'answer_count')
        read_only_fields = ('id', 'question_count', 'answer_count')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class AuthTokenSerializer(serializers.Serializer):
    """Custom token authentication serializer"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Authenticate and return user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )

        if not user:
            msg = "Unable to authenticate with provided credentials"
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
