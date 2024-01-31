from django.shortcuts import render


def entry_not_found(request, exception, template_name="404.html"):
    """
    Render the custom 404 error page.
    :param request:
    :param exception:
    :param template_name:
    :return: render the template
    """
    return render(request, template_name)


def server_error(request, template_name="500.html"):
    """
    Render the custom 500 error page.
    :param request:
    :param template_name:
    :return: render the template
    """
    return render(request, template_name)


def permission_denied(request, exception, template_name="403.html"):
    """
    Render the custom 403 error page.
    :param request:
    :param exception:
    :param template_name:
    :return: render the template
    """
    return render(request, template_name)


def bad_request(request, exception, template_name="400.html"):
    """
    Render the custom 400 error page.
    :param request:
    :param exception:
    :param template_name:
    :return: render the template
    """
    return render(request, template_name)
