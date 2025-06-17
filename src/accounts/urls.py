from django.urls import path
from accounts.views import send_login_email, login
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("send_login_email", send_login_email, name="send_login_email"),
    path("login", login, name="login"),
    path("logout", auth_views.LogoutView.as_view(next_page="/"), name="logout")

]
