from django.urls import path, include
from chat import views as chat_views

urlpatterns = [
    path("chat/", chat_views.chatPage, name="chat-page"),
    path("active_users/", chat_views.activeUser, name="active-users"),
]