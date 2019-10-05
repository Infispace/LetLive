from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.views.generic import ListView

from home.models import Article

class IndexView(ListView):
    model = Article
    template_name = 'home/index.html'
    context_object_name = 'latest_articles_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'index'
        return context

    def get_queryset(self):
        return Article.objects.published()
