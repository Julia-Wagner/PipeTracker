from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = "home/index.html"


class Statistics(TemplateView):
    template_name = "home/statistics.html"
