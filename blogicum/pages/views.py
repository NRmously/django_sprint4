from django.conf import settings
from django.shortcuts import render


def handler403(request, reason=''):
    return render(request, 'pages/403csrf.html', status=settings.ACCESS_DENIED)


def handler404(request, exception):
    return render(request, 'pages/404.html', status=settings.PAGE_NOT_FOUND)


def handler500(request):
    return render(request, 'pages/500.html', status=settings.SERVER_ERROR)
