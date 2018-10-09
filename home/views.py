from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views import generic

from .models import Author, Topic, Article
# Create your views here.

class IndexView(generic.ListView):
    model = Article
    template_name = 'home/index.html'
    context_object_name = 'latest_articles_list'

    #def get_queryset(self):
        #Author.objects.all()

class TopicView(generic.DetailView):
    model = Topic
    template_name = 'home/topic.html'

    def get(self, request, topic_id=0):
        return HttpResponse('topic view'+
            reverse('home:topic_default')
        )

class ArticleView(generic.DetailView):
    model = Article
    template_name = 'home/article.html'

    def get(self, request, article_id=0):
        return HttpResponse('article view')

    def post(self, request, *args, **kwargs):
        pass

class UserView(generic.DetailView):
    model = Author
    template_name = 'home/user.html'

    def get(self, request, user_id=0):
        return HttpResponse('user view')

    def userLogin(request):
        user = authenticate(username='ken', password='myPass')
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponse('user loged in')
        else:
            return HttpResponse('user error')

    @login_required(login_url='/user/login')
    def userLogout(request):
        if request.user.is_authenticated:
            logout(request)
            return HttpResponse('user loged out')
        else:
            # Redirect to a success page.
            return HttpResponse('user not loged in')
