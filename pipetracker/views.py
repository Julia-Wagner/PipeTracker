from django.shortcuts import render


# custom 404 page
def entry_not_found(request, exception, template_name="404.html"):
    return render(request, template_name)


# custom 500 page
def server_error(request, template_name="500.html"):
    return render(request, template_name)


# custom 403 page
def permission_denied(request, exception, template_name="403.html"):
    return render(request, template_name)


# custom 400 page
def bad_request(request, exception, template_name="400.html"):
    return render(request, template_name)
