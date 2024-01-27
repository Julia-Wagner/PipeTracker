"""
URL configuration for pipetracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("", include("home.urls")),
    path("stock/", include("stock.urls")),
    path("delivery/", include("delivery.urls")),
    path("basket/", include("basket.urls")),

    # add robots.txt
    # https://adamj.eu/tech/2020/02/10/robots-txt/
    path("robots.txt", TemplateView.as_view(template_name="robots.txt",
                                            content_type="text/plain")),
]

# custom error pages
handler404 = "pipetracker.views.entry_not_found"
handler500 = "pipetracker.views.server_error"
handler403 = "pipetracker.views.permission_denied"
handler400 = "pipetracker.views.bad_request"
