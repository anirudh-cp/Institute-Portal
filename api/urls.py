from django.urls import path, include, register_converter

from api.Views.Administrators import AdministratorAllApiView, AdministratorSingleApiView
from api.Views.Preferences import preferenceAllApiView, preferenceSingleApiView

from .Views.Account import *
from .Views.Course import *
from .Views.Faculty import *
from .Views.Preferences import *


urlpatterns = [
    path('account/login', ObtainAuthTokenView.as_view()),
    path('account/register', registration_view),
    
    path('course', CourseAllApiView.as_view()),
    path('course/<course_code>', CourseSingleApiView.as_view()),
    
    path('faculty', FacultyAllApiView.as_view()),
    path('faculty/<int:emp_id>', FacultySingleApiView.as_view()),
    
    path('administrator', AdministratorAllApiView.as_view()),
    path('administrator/<int:admin_id>', AdministratorSingleApiView.as_view()),
    
    path('preference', preferenceAllApiView.as_view()),
    path('preference/<int:emp_id>', preferenceSingleApiView.as_view())
]
