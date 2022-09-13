from django.urls import path, include, register_converter
from .Views.Account import *


urlpatterns = [
    path('account/login', ObtainAuthTokenView.as_view()),
    path('account/register', registration_view),
]
