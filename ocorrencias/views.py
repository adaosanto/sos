from operator import attrgetter

from django.http import JsonResponse
from django.views.generic import DetailView, TemplateView

from app.views import LoginRequiredMixin

from .models import Ocorrencia


class ListOcorrenciasView(LoginRequiredMixin, TemplateView):
    template_name = "ocorrencias/index.html"

    def get(self, request, *args, **kwargs):
        format = request.GET.get("f")
        if format == "json":
            ocorrencias = Ocorrencia.objects.all()
            fields_mapping = {
                "ID": "id",
                "VITIMA": "vitima.nome",
                "SUSPEITO": "vitima.suspeito",
                "ENDERECO": "vitima.endereco",
                "ATIVO": "status_flag",
            }

            data = [
                [attrgetter(field)(ocorrencia) for field in fields_mapping.values()]
                for ocorrencia in ocorrencias
            ]

            return JsonResponse(
                {
                    "recordsTotal": len(data),
                    "columns": list(fields_mapping.keys()),
                    "data": data,
                }
            )

        return super().get(request, *args, **kwargs)


class DetailOCorrenciasView(LoginRequiredMixin, DetailView):
    """
    Exibe os detalhes de uma vítima específica.
    """

    model = Ocorrencia
    template_name = "ocorrencias/modal_ocorrencias.html"
