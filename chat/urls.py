from django.urls import path, include
from chat import views as chat_views

urlpatterns = [
    path("chat/<int:group_id>/", chat_views.chatPage, name="chat-page"),
    path("create-group/", chat_views.createGroup, name="create-group"),
    path("", chat_views.activeUser, name="active-users"),
]