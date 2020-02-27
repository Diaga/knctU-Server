from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, \
    BaseUserManager

from model_utils import FieldTracker


class Tag(models.Model):
    """Tag model"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        app_label = 'forum'
        default_related_name = 'tags'

    def __str__(self):
        return self.name


def user_avatar_path(instance, file_name):
    """Return file path"""
    return file_name


class UserManager(BaseUserManager):
    """Manager for User model"""

    def create_user(self, email, password, **kwargs):
        """Creates and saves the user"""
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(email=email.lower(), **kwargs)
        user.set_password(password)

        user.save()

        return user

    def create_superuser(self, email, password):
        """Creates and saves the superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True

        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User model"""
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    avatar = models.FileField(blank=True, null=True,
                              upload_to=user_avatar_path)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    tags = models.ManyToManyField(Tag, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        app_label = 'user'
        default_related_name = 'users'

    def __str__(self):
        return self.email


class InfoUser(models.Model):
    """Info User model"""
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=255)
    has_upvoted = models.BooleanField(default=False)
    has_viewed = models.BooleanField(default=False)
    has_shared = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    question = models.ForeignKey('Question', on_delete=models.CASCADE,
                                 null=True)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE,
                               null=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE,
                                null=True)
    reply = models.ForeignKey('Reply', on_delete=models.CASCADE,
                              null=True)

    tracker = FieldTracker()

    class Meta:
        app_label = 'forum'
        default_related_name = 'info_user_set'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        instance = super(InfoUser, self).save(
            force_insert=force_insert, force_update=force_update, using=using,
            update_fields=update_fields
        )
        changed_fields = self.tracker.changed()
        if len(changed_fields) != 0:
            if self.question:
                QuestionHandler.update_question('UPDATE_QUESTION',
                                                self.question)
            elif self.answer:
                QuestionHandler.update_question('UPDATE_QUESTION', self.answer.question)
            elif self.comment:
                QuestionHandler.update_question('UPDATE_QUESTION', self.comment.answer.question)
            elif self.reply:
                QuestionHandler.update_question('UPDATE_QUESTION', self.reply.comment.answer.question)

        return instance

    def __str__(self):
        return f'InfoUser: {self.user.name}'


class Question(models.Model):
    """Question model"""
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    tags = models.ManyToManyField(Tag, blank=True)

    tracker = FieldTracker()

    class Meta:
        app_label = 'forum'
        default_related_name = 'questions'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        instance = super(Question, self).save(
            force_insert=force_insert, force_update=force_update, using=using,
            update_fields=update_fields
        )
        changed_fields = self.tracker.changed()
        if len(changed_fields) != 0:
            QuestionHandler.update_question('UPDATE_QUESTION',
                                            self)

        return instance

    def __str__(self):
        return self.text


class Answer(models.Model):
    """Answer model"""
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    tracker = FieldTracker()

    class Meta:
        app_label = 'forum'
        default_related_name = 'answers'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        instance = super(Answer, self).save(
            force_insert=force_insert, force_update=force_update, using=using,
            update_fields=update_fields
        )
        changed_fields = self.tracker.changed()
        if len(changed_fields) != 0:
            QuestionHandler.update_question('UPDATE_QUESTION', self.question)

        return instance

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Comment model"""
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    tracker = FieldTracker()

    class Meta:
        app_label = 'forum'
        default_related_name = 'comments'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        instance = super(Comment, self).save(
            force_insert=force_insert, force_update=force_update, using=using,
            update_fields=update_fields
        )
        changed_fields = self.tracker.changed()
        if len(changed_fields) != 0:
            QuestionHandler.update_question(
                'UPDATE_QUESTION', self.answer.question)

        return instance

    def __str__(self):
        return self.text


class Reply(models.Model):
    """Reply model"""
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    tracker = FieldTracker()

    class Meta:
        app_label = 'forum'
        default_related_name = 'replies'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        instance = super(Reply, self).save(
            force_insert=force_insert, force_update=force_update, using=using,
            update_fields=update_fields
        )
        changed_fields = self.tracker.changed()
        if len(changed_fields) != 0:
            QuestionHandler.update_question(
                'UPDATE_QUESTION', self.comment.answer.question)

        return instance

    def __str__(self):
        return self.text


class ChatRoom(models.Model):
    """ChatRoom model"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, default='@bidirectional')
    users = models.ManyToManyField(User)

    tracker = FieldTracker()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        instance = super(ChatRoom, self).save(
            force_insert=force_insert, force_update=force_update, using=using,
            update_fields=update_fields
        )
        changed_fields = self.tracker.changed()
        if len(changed_fields) != 0:
            ChatRoomHandler.update_chat_room(
                'UPDATE_CHAT_ROOM', self)

        return instance

    class Meta:
        app_label = 'chat'
        default_related_name = 'chat_rooms'

    def __str__(self):
        return self.name


class Message(models.Model):
    """Message model"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    tracker = FieldTracker()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        instance = super(Message, self).save(
            force_insert=force_insert, force_update=force_update, using=using,
            update_fields=update_fields
        )
        if self.message_users.count() == 0:
            MessageUser.objects.bulk_create([
                MessageUser(
                    user=user_itr,
                    is_read=False if user_itr.id != self.user.id else True,
                    message=self)
                for user_itr in self.chat_room.users.all()
            ])
        changed_fields = self.tracker.changed()
        if len(changed_fields) != 0:
            ChatRoomHandler.update_chat_room(
                'UPDATE_CHAT_ROOM', self.chat_room)

        return instance

    class Meta:
        app_label = 'chat'
        default_related_name = 'messages'

    def __str__(self):
        return self.text


class MessageUser(models.Model):
    """MessageUser model generated for every user in the user group"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    tracker = FieldTracker()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        instance = super(MessageUser, self).save(
            force_insert=force_insert, force_update=force_update, using=using,
            update_fields=update_fields
        )
        changed_fields = self.tracker.changed()
        if len(changed_fields) != 0:
            ChatRoomHandler.update_chat_room(
                'UPDATE_CHAT_ROOM', self.message.chat_room)

        return instance

    class Meta:
        app_label = 'chat'
        default_related_name = 'message_users'

    def __str__(self):
        return f'{self.message.text} - {self.user.name}'


from forum.handlers import QuestionHandler
from chat.handlers import ChatRoomHandler
