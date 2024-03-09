from django.urls import include, path

from .views import HomePageView

urlpatterns = [
    path("users/", include("users.urls")),
    path("vitimas/", include("vitimas.urls")),
    path("ocorrencias/", include("ocorrencias.urls")),
    path("api/", include("apimobilie.urls")),
    path("", HomePageView.as_view(), name="home"),
]
