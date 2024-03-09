from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import Group

class LoginRequiredMixin(object):
    """
    Um mixin para exigir autenticação de usuário antes de acessar uma visualização.
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "home/index.html"

class OnlyAdminPermissionMixin(LoginRequiredMixin, View):
    """
    Um mixin para exigir permissões de administrador antes de acessar uma visualização.
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.filter(name='admin').exists() or self.request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'Você não tem permissão para acessar esta página.')
        return redirect('home')
        