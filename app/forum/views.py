from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Question, Answer, Comment, Reply, InfoUser
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
    
    def view_question_by_id(self, request, *args, **kwargs):
        """Wrapper around retrieve method for view set distinction"""
        return self.retrieve(request, *args, **kwargs)

    def update_question_by_id(self, request, *args, **kwargs):
        """Wrapper around update method for view set distinction"""
        return self.partial_update(request, *args, **kwargs)

    def destroy_question_by_id(self, request, *args, **kwargs):
        """Wrapper around destroy method for view set distinction"""
        return self.destroy(request, *args, **kwargs)


class AnswerViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin):
    """View set for Answer model"""

    authentication_classes = [TokenAuthentication, ]

    permission_classes = [IsAuthenticated, ]

    serializer_class = serializers.AnswerSerializer

    queryset = Answer.objects.all()

    def create_answer(self, request, *args, **kwargs):
        """Wrapper around create method for view set distinction"""
        return self.create(request, *args, **kwargs)


class AnswerDetailViewSet(viewsets.GenericViewSet,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin):
    """Detail view set for Answer model"""

    authentication_classes = [TokenAuthentication, ]

    permission_classes = [IsAuthenticated, ]

    serializer_class = serializers.AnswerSerializer

    queryset = Answer.objects.all()

    def get_queryset(self):
        """Enforce scope"""
        return super(AnswerDetailViewSet, self).get_queryset().filter(
            user=self.request.user
        ).all()

    def view_answer_by_id(self, request, *args, **kwargs):
        """Wrapper around retrieve method for view set distinction"""
        return self.retrieve(request, *args, **kwargs)

    def update_answer_by_id(self, request, *args, **kwargs):
        """Wrapper around update method for view set distinction"""
        return self.partial_update(request, *args, **kwargs)

    def destroy_answer_by_id(self, request, *args, **kwargs):
        """Wrapper around destroy method for view set distinction"""
        return self.destroy(request, *args, **kwargs)


class CommentViewSet(viewsets.GenericViewSet,
                     mixins.CreateModelMixin):
    """View set for Comment model"""

    authentication_classes = [TokenAuthentication, ]

    permission_classes = [IsAuthenticated, ]

    serializer_class = serializers.CommentSerializer

    queryset = Comment.objects.all()

    def create_comment(self, request, *args, **kwargs):
        """Wrapper around create method for view set distinction"""
        return self.create(request, *args, **kwargs)


class CommentDetailViewSet(viewsets.GenericViewSet,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin):
    """Detail view set for Comment model"""

    authentication_classes = [TokenAuthentication, ]

    permission_classes = [IsAuthenticated, ]

    serializer_class = serializers.CommentSerializer

    queryset = Comment.objects.all()

    def get_queryset(self):
        """Enforce scope"""
        return super(CommentDetailViewSet, self).get_queryset().filter(
            user=self.request.user
        ).all()

    def view_comment_by_id(self, request, *args, **kwargs):
        """Wrapper around retrieve method for view set distinction"""
        return self.retrieve(request, *args, **kwargs)

    def update_comment_by_id(self, request, *args, **kwargs):
        """Wrapper around update method for view set distinction"""
        return self.partial_update(request, *args, **kwargs)

    def destroy_comment_by_id(self, request, *args, **kwargs):
        """Wrapper around destroy method for view set distinction"""
        return self.destroy(request, *args, **kwargs)


class ReplyViewSet(viewsets.GenericViewSet,
                   mixins.CreateModelMixin):
    """View set for Reply model"""

    authentication_classes = [TokenAuthentication, ]

    permission_classes = [IsAuthenticated, ]

    serializer_class = serializers.ReplySerializer

    queryset = Reply.objects.all()

    def create_reply(self, request, *args, **kwargs):
        """Wrapper around create method for view set distinction"""
        return self.create(request, *args, **kwargs)


class ReplyDetailViewSet(viewsets.GenericViewSet,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin):
    """Detail view set for Reply model"""

    authentication_classes = [TokenAuthentication, ]

    permission_classes = [IsAuthenticated, ]

    serializer_class = serializers.ReplySerializer

    queryset = Reply.objects.all()

    def get_queryset(self):
        """Enforce scope"""
        return super(ReplyDetailViewSet, self).get_queryset().filter(
            user=self.request.user
        ).all()

    def view_reply_by_id(self, request, *args, **kwargs):
        """Wrapper around retrieve method for view set distinction"""
        return self.retrieve(request, *args, **kwargs)

    def update_reply_by_id(self, request, *args, **kwargs):
        """Wrapper around update method for view set distinction"""
        return self.partial_update(request, *args, **kwargs)

    def destroy_reply_by_id(self, request, *args, **kwargs):
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
        return self.partial_update(request, *args, **kwargs)
