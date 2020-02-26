from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Question, InfoUser
from . import serializers


class QuestionViewSet(viewsets.GenericViewSet,
                      mixins.CreateModelMixin):
    """View set for Question model"""

    authentication_classes = [TokenAuthentication, ]

    permission_classes = [IsAuthenticated, ]

    queryset = Question.objects.all()

    serializer_class = serializers.QuestionSerializer

    def view_question(self, request, *args, **kwargs):
        """Return objects"""
        serializer = self.get_serializer(
            self.get_queryset(), many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def view_home_question(self, request, *args, **kwargs):
        """Return questions to show at home"""
        serializer = self.get_serializer(
            self.get_queryset().filter(
                answers__isnull=False
            ).all(), many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create_question(self, request, *args, **kwargs):
        """Wrapper around create method for view set distinction"""
        return self.create(request, *args, **kwargs)


class QuestionDetailViewSet(viewsets.GenericViewSet,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin):
    """Detail view set for Question model"""

    authentication_classes = [TokenAuthentication, ]

    permission_classes = [IsAuthenticated, ]

    queryset = Question.objects.all()

    serializer_class = serializers.QuestionSerializer

    def get_queryset(self):
        """Enforce scope"""
        return super(QuestionDetailViewSet, self).get_queryset().filter(
            user=self.request.user
        ).all()

    def view_question_by_id(self, request, *args, **kwargs):
        """Wrapper around retrieve method for view set distinction"""
        return self.retrieve(request, *args, **kwargs)

    def update_question_by_id(self, request, *args, **kwargs):
        """Wrapper around update method for view set distinction"""
        return self.partial_update(request, *args, **kwargs)

    def destroy_question_by_id(self, request, *args, **kwargs):
        """Wrapper around destroy method for view set distinction"""
        return self.destroy(request, *args, **kwargs)


class InfoUserDetailViewSet(viewsets.GenericViewSet,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin):
    """Detail view set for Info User"""

    authentication_classes = [TokenAuthentication, ]

    permission_classes = [IsAuthenticated, ]

    serializer_class = serializers.InfoUserSerializer

    queryset = InfoUser.objects.all()

    def get_queryset(self):
        """Return own info user"""
        return super(InfoUserDetailViewSet, self).get_queryset().filter(
            user=self.request.user
        ).all()

    def view_info_user_by_id(self, request, *args, **kwargs):
        """Wrapper around retrieve method for view set distinction"""
        return self.retrieve(request, *args, **kwargs)

    def update_info_user_by_id(self, request, *args, **kwargs):
        """Wrapper around update method for view set distinction"""
        return self.update(request, *args, **kwargs)
