from django.urls import path

from core.views import CoreView

urlpatterns = [
    path("", CoreView.as_view(), name="index"),
]
