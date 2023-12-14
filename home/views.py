from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = "home/index.html"


class Dashboard(TemplateView):
    template_name = "home/dashboard.html"
