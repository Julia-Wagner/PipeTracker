from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import Index, Statistics

urlpatterns = [
    path("", Index.as_view(), name="home"),
    path("statistics/", login_required(Statistics.as_view()),
         name="statistics"),
]
