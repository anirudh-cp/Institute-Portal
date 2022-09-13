from django.urls import path, include, register_converter
from .Views.Account import *
from .Views.Course import *


urlpatterns = [
    path('account/login', ObtainAuthTokenView.as_view()),
    path('account/register', registration_view),
    
    path('course', CourseAllApiView.as_view()),
    path('course/<course_code>', CourseSingleApiView.as_view()),
]
