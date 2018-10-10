from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views import generic

from .models import Topic, Article
# Create your views here.

class IndexView(generic.ListView):
    model = Article
    template_name = 'home/index.html'
    context_object_name = 'latest_articles_list'

    #def get_queryset(self):
        #Article.objects.all()

class TopicView(generic.DetailView):
    model = Topic
    template_name = 'home/topic.html'

    def get(self, request, topic_id=0):
        if topic_id > 0:
            return HttpResponse('topic ' +str(topic_id))
        else:
            return HttpResponse('topic view'+
                reverse('home:topic_default')
            )

class ArticleView(generic.DetailView):
    model = Article
    template_name = 'home/article.html'

    def get(self, request, article_id=0):
        if article_id > 0:
            return HttpResponse('article ' +str(article_id))
        else:
            return HttpResponse('article view')


    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        pass

class UserView(generic.DetailView):
    #model = User
    template_name = 'home/user.html'

    @method_decorator(login_required)
    def get(self, request, user_id=0):
        if user_id > 0:
            return HttpResponse('user view '+str(user_id))
        else:
            return HttpResponse('user view '+request.user.username)

    def userLogin(request, next=''):
        user = authenticate(username='ken', password='myPass')
        if user is not None:
            login(request, user)
            if next is not '':
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect(reverse('home:index'))
        else:
            return HttpResponse('user error')

    def userLogout(request):
        if request.user.is_authenticated:
            logout(request)
            return HttpResponseRedirect(reverse('home:index'))
        else:
            return HttpResponse('user error')
