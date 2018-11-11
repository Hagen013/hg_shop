from django.views.generic import TemplateView
from django.shortcuts import redirect


class LoginView(TemplateView):
    template_name = "admin/login.html"


class AdminAppView(TemplateView):
    template_name = "admin/app.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super(AdminAppView, self).get(request, *args, **kwargs)
        else:
            return redirect("md-admin:login")