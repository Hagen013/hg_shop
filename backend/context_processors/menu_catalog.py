from django.template.context_processors import request
from core.models import CategoryPage


def menu(request):
    context = {}
    context['nodes'] = CategoryPage.public.all()
    return context
