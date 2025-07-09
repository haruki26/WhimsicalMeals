from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class CoreView(TemplateView):
    def __init__(self) -> None:
        pass

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "core/index.html")
