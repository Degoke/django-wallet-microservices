from django.urls import include, path

from core.views import CreateUserView
from core.views import LoginView
from core.views import GetUsersView

urlpatterns = [
    path('signup/', CreateUserView.as_view(), name='create user'),
    path('login/', LoginView.as_view(), name='login user'),
    path('all/', GetUsersView.as_view(), name='get all user'),
]