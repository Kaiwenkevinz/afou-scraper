from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import api

urlpatterns = [
    path('schedules/', api.schedules),
]

urlpatterns = format_suffix_patterns(urlpatterns)