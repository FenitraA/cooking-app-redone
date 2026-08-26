from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. My first Django API call")