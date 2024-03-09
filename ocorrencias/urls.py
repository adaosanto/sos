from django.urls import path

from .views import DetailOCorrenciasView, ListOcorrenciasView

urlpatterns = [
    path("", ListOcorrenciasView.as_view(), name="ocorrencias"),
    path("<int:pk>", DetailOCorrenciasView.as_view(), name="ocorrencias-detail"),
]
