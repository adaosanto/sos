from django.urls import path

from .views import ChangeVitimaView, CreateVitimaView, DetailVitimaView, ListVitimasView

urlpatterns = [
    path("new/", CreateVitimaView.as_view(), name="vitimas-new"),
    path("", ListVitimasView.as_view(), name="vitimas"),
    path("<int:pk>/", ChangeVitimaView.as_view(), name="vitimas-edit"),
    path("<int:pk>/detail/", DetailVitimaView.as_view(), name="vitima-detail"),
]
