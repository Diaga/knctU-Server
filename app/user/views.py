from rest_framework import viewsets, status, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from core.models import User, Tag
from . import serializers


class UserViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin):
    """View set for User model"""

    authentication_classes = [TokenAuthentication, ]

    permission_classes = [IsAuthenticated, ]

    queryset = User.objects.all()

    serializer_class = serializers.UserSerializer

    def view_user(self, request, *args, **kwargs):
        """Return users"""
        serializer = self.get_serializer(
            self.request.user
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create_user(self, request, *args, **kwargs):
        """Wrapper around create method for view set distinction"""
        return self.create(request, *args, **kwargs)


class UserDetailViewSet(viewsets.GenericViewSet,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    """Detail view set for User model"""

    authentication_classes = [TokenAuthentication, ]

    permission_classes = [IsAuthenticated, ]

    queryset = User.objects.all()

    serializer_class = serializers.UserSerializer

    def view_user_by_id(self, request, *args, **kwargs):
        """Wrapper around retrieve method for view set distinction"""
        return self.retrieve(request, *args, **kwargs)

    def update_user_by_id(self, request, *args, **kwargs):
        """Wrapper around update method for view set distinction"""
        return self.partial_update(request, *args, **kwargs)

    def destroy_user_by_id(self, request, *args, **kwargs):
        """Wrapper around destroy method for view set distinction"""
        return self.destroy(request, *args, **kwargs)


class TagViewSet(viewsets.GenericViewSet):
    """View set for Tag model"""

    authentication_classes = [TokenAuthentication, ]

    permission_classes = [IsAuthenticated, ]

    serializer_class = serializers.TagSerializer

    queryset = Tag.objects.all()

    def view_tag(self, request, *args, **kwargs):
        """Return all tags"""
        serializer = self.get_serializer(
            self.get_queryset(), many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthTokenViewSet(ObtainAuthToken):
    """Custom Token Authentication View Set"""

    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
