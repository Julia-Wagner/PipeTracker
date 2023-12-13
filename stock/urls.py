from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import AddCategory

urlpatterns = [
    path("", login_required(AddCategory.as_view()),
         name="add_category"),
]
