from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView

from app.views import LoginRequiredMixin, OnlyAdminPermissionMixin

from .forms import VitimaChangeForm, VitimaCreateForm
from .models import Vitima


class ListVitimasView(OnlyAdminPermissionMixin, LoginRequiredMixin, TemplateView):
    template_name = "vitimas/index.html"

    def get(self, request, *args, **kwargs):
        format = request.GET.get("f")

        if format == "json":
            users = Vitima.objects.all()
            fields_mapping = {
                "ID": "id",
                "Nome": "nome",
                "SUSPEITO": "suspeito",
                "CPF": "cpf",
                "ENDERECO": "endereco",
                "ATIVO": "status_flag",
            }
            data = [
                [getattr(user, field) for field in fields_mapping.values()]
                for user in users
            ]

            return JsonResponse(
                {
                    "recordsTotal": len(data),
                    "columns": list(fields_mapping.keys()),
                    "data": data,
                },
            )

        return super().get(request, *args, **kwargs)


class CreateVitimaView(OnlyAdminPermissionMixin, LoginRequiredMixin, CreateView):
    template_name = "vitimas/cadastro.html"
    form_class = VitimaCreateForm
    success_url = reverse_lazy("vitimas")

    def form_valid(self, form):
        messages.success(self.request, "Cadastrado com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request, error)
        return redirect("vitimas")


class ChangeVitimaView(OnlyAdminPermissionMixin, LoginRequiredMixin, UpdateView):
    model = Vitima
    form_class = VitimaChangeForm
    template_name = "vitimas/editar.html"
    success_url = reverse_lazy("vitimas")

    def form_valid(self, form):
        messages.success(self.request, "Alterado com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Erro no campo '{field}': {error}")
        return redirect("vitimas")


class DetailVitimaView(OnlyAdminPermissionMixin, LoginRequiredMixin, DetailView):
    """
    Exibe os detalhes de uma vítima específica.
    """

    model = Vitima
    template_name = "vitimas/modal_vitimas.html"
