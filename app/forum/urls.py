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
    )
]

router.register('forum', views.QuestionViewSet)
router.register('forum', views.QuestionDetailViewSet)

urlpatterns = [
    path('', include(router.urls))
]
