from django.urls import path, include
from account import views as account_views

urlpatterns = [
    # authentication section
    path("login/", account_views.login_view, name="login-user"),
    path("logout/", account_views.logout_view, name="logout-user"),
    path('register/', account_views.register, name='register'),
]