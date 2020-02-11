from django.urls import path, include
from rest_framework.routers import Route

from app.urls import router
from . import views

app_name = 'chat'

router.routes += [
    # ChatRoom View Route
    Route(
        url=r'^chat{trailing_slash}room{trailing_slash}$',
        mapping={
            'get': 'view_chat_room'
        },
        name='chat_room-view',
        detail=False,
        initkwargs={'suffix': 'View'}
    ),
]

router.register('chat', views.ChatRoomViewSet)

urlpatterns = [
    path('', include(router.urls))
]
