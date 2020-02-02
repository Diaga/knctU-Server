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
    )
]

router.register('forum', views.QuestionViewSet)
router.register('forum', views.QuestionDetailViewSet)

urlpatterns = [
    path('', include(router.urls))
]
