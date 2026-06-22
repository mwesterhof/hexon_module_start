from django.urls import path

from .views import HexonMutateView


urlpatterns = [
    path("api/mutate/", HexonMutateView.as_view()),
]