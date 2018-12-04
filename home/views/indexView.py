from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.views import generic

from ..models.articleModel import Article

class IndexView(generic.ListView):
    model = Article
    template_name = 'home/index.html'
    context_object_name = 'latest_articles_list'

    #def get_queryset(self):
        #Article.objects.all()
