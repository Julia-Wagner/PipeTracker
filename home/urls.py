from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import Index, Dashboard

urlpatterns = [
    path("", Index.as_view(), name="home"),
    path("dashboard/", login_required(Dashboard.as_view()),
         name="dashboard"),
]
