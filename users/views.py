from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from app.views import LoginRequiredMixin, OnlyAdminPermissionMixin

from .forms import (
    UserCustomChangeForm,
    UserCustomUserCretionForm,
    UserLoginForm,
    UserMeCustomChangeForm,
)


class LoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("home")
    form_class = UserLoginForm

    def form_invalid(self, form: UserLoginForm):
        for error in form.errors.values():
            messages.error(self.request, error)
        return super().form_invalid(form)


class AboutMeView(LoginRequiredMixin, TemplateView):
    template_name = "users/sobreme.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client_ip"] = self.request.META["REMOTE_ADDR"]
        context["expire_in"] = self.request.session.get_expiry_date()
        return context


class ChangeMeView(LoginRequiredMixin, UpdateView):
    form_class = UserMeCustomChangeForm
    success_url = reverse_lazy("aboutme")
    template_name = "users/editame.html"

    def get_object(self, queryset=None):
        return self.request.user

    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request, error)
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, "Alterado com sucesso")
        return super().form_valid(form)


class ListUsersView(OnlyAdminPermissionMixin, LoginRequiredMixin, TemplateView):
    template_name = "users/index.html"

    def get(self, request, *args, **kwargs):
        format = request.GET.get("f")

        if format == "json":
            users = get_user_model().objects.all()
            fields_mapping = {
                "ID": "id",
                "Nome": "nome",
                "E-mail": "email",
                "Telefone": "telefone",
                "CPF": "cpf",
                "Status": "status_flag",
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
                }
            )

        return super().get(request, *args, **kwargs)


class ChangeUserView(OnlyAdminPermissionMixin, LoginRequiredMixin, UpdateView):
    template_name = "users/detalhes-user.html"
    form_class = UserCustomChangeForm
    model = get_user_model()
    success_url = reverse_lazy("users")

    def form_valid(self, form):
        messages.success(self.request, "Alterado com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request, error)
        return redirect("users")


class CreateUserView(OnlyAdminPermissionMixin, LoginRequiredMixin, CreateView):
    template_name = "users/cadastro.html"
    form_class = UserCustomUserCretionForm
    success_url = reverse_lazy("users")

    def form_valid(self, form):
        messages.success(self.request, "Cadastrado com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request, error)
        return redirect("users")
