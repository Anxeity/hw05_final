from django.urls import path
from django.contrib.auth import views

from . import views

app_name = 'users'

urlpatterns = [
    path(
        'signup/',
        views.SignUp.as_view(),
        name='signup'
    ),
]
