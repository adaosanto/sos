from django.urls import path

from .views import LoginAPIView, OcorrenciaAPIView

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login-api-view"),
    path("ocorrencia/", OcorrenciaAPIView.as_view(), name="ocorrencia-api-view"),
]
