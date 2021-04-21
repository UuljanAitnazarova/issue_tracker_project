from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView
from accounts.views import RegisterView, UserDetailView, UsersListView, UserUpdateView, UserPasswordChangeView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', RegisterView.as_view(), name='registration'),
    path('profile/', UserUpdateView.as_view(), name='update_profile'),
    path('<int:pk>/', UserDetailView.as_view(), name='detail'),
    path('users/', UsersListView.as_view(), name='users'),
    path('change_password/', UserPasswordChangeView.as_view(), name='change_password'),
]