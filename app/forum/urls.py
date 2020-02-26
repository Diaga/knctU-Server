from django.urls import path, include
from rest_framework.routers import Route

from app.urls import router
from . import views

app_name = 'forum'

router.routes += [
    # Question View Set
    Route(
        url=r'^forum{trailing_slash}question{trailing_slash}$',
        mapping={
            'get': 'view_question',
            'post': 'create_question'
        },
        name='question-view',
        detail=False,
        initkwargs={'suffix': 'View'}
    ),

    # Question Home Route
    Route(
        url=r'^forum{trailing_slash}home{trailing_slash}question'
            r'{trailing_slash}$',
        mapping={
            'get': 'view_home_question'
        },
        name='question-home-view',
        detail=False,
        initkwargs={'suffix': 'Home View'}
    ),

    # Question Detail View Set
    Route(
        url=r'^forum{trailing_slash}question{trailing_slash}{lookup}'
            r'{trailing_slash}$',
        mapping={
            'get': 'view_question_by_id',
            'patch': 'update_question_by_id',
            'delete': 'destroy_question_by_id'
        },
        name='question-detail',
        detail=True,
        initkwargs={'suffix': 'Detail'}
    ),

    # Answer View Route
    Route(
        url=r'^forum{trailing_slash}answer{trailing_slash}$',
        mapping={
            'post': 'create_answer'
        },
        name='answer-view',
        detail=False,
        initkwargs={'suffix': 'View'}
    ),

    # Answer Detail Route
    Route(
        url=r'^forum{trailing_slash}answer{trailing_slash}{lookup}'
            r'{trailing_slash}$',
        mapping={
            'get': 'view_answer_by_id',
            'patch': 'update_answer_by_id',
            'delete': 'destroy_answer_by_id'
        },
        name='answer-detail',
        detail=True,
        initkwargs={'suffix': 'Detail'}
    ),

    # Comment View Route
    Route(
        url=r'^forum{trailing_slash}comment{trailing_slash}$',
        mapping={
            'post': 'create_comment'
        },
        name='comment-view',
        detail=False,
        initkwargs={'suffix': 'View'}
    ),

    # Comment Detail Route
    Route(
        url=r'^forum{trailing_slash}comment{trailing_slash}{lookup}'
            r'{trailing_slash}$',
        mapping={
            'get': 'view_comment_by_id',
            'patch': 'update_comment_by_id',
            'delete': 'destroy_comment_by_id'
        },
        name='comment-detail',
        detail=True,
        initkwargs={'suffix': 'Detail'}
    ),

    # Reply View Route
    Route(
        url=r'^forum{trailing_slash}reply{trailing_slash}$',
        mapping={
            'post': 'create_reply'
        },
        name='reply-view',
        detail=False,
        initkwargs={'suffix': 'View'}
    ),

    # Reply Detail Route
    Route(
        url=r'^forum{trailing_slash}reply{trailing_slash}{lookup}'
            r'{trailing_slash}$',
        mapping={
            'get': 'view_reply_by_id',
            'patch': 'update_reply_by_id',
            'delete': 'destroy_reply_by_id'
        },
        name='reply-detail',
        detail=True,
        initkwargs={'suffix': 'Detail'}
    ),

    # Info User Detail View Set
    Route(
        url=r'^forum{trailing_slash}info{trailing_slash}user{trailing_slash}'
            r'{lookup}{trailing_slash}$',
        mapping={
            'get': 'view_info_user_by_id',
            'patch': 'update_info_user_by_id',
        },
        name='info-user-detail',
        detail=True,
        initkwargs={'suffix': 'Detail'}
    ),
]

router.register('forum', views.QuestionViewSet)
router.register('forum', views.QuestionDetailViewSet)
router.register('forum', views.AnswerViewSet)
router.register('forum', views.AnswerDetailViewSet)
router.register('forum', views.CommentViewSet)
router.register('forum', views.CommentDetailViewSet)
router.register('forum', views.ReplyViewSet)
router.register('forum', views.ReplyDetailViewSet)

urlpatterns = [
    path('', include(router.urls))
]
