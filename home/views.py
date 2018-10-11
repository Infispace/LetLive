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

from .models import Topic, Article
from .forms import LoginForm, RegisterForm, ArticleForm
# Create your views here.

class IndexView(generic.ListView):
    model = Article
    template_name = 'home/index.html'
    context_object_name = 'latest_articles_list'

    #def get_queryset(self):
        #Article.objects.all()

class TopicView(generic.TemplateView):
    template_name = 'home/topic.html'
    topic = None
    topic_list = None

    def get(self, request, topic_id=0):
        if topic_id > 0:
            self.topic = get_object_or_404(Topic, pk=topic_id)
        else:
            self.topic_list = Topic.objects.all()

        return render(request, self.template_name, {
            'topic': self.topic, 'topic_list': self.topic_list
        })

class ArticleView(generic.TemplateView):
    template_name = 'home/article.html'
    form = None
    article_to_edit = None
    article_list = None

    def get(self, request, article_id=0, page='article'):
        if page is 'article_new':
            self.form = ArticleForm()
        elif page is 'article_edit':
            article_to_edit =  get_object_or_404(Article, pk=article_id)
            self.form = ArticleForm(instance=article_to_edit)
        else:
            if article_id > 0:
                self.article_to_edit =  get_object_or_404(Article, pk=article_id)
            else:
                # render some articles in my blog
                self.article_list = Article.objects.all()

        return render(request, self.template_name, {
            'page': page,
            'form': self.form,
            'article': self.article_to_edit,
            'blog_article_list': self.article_list
        })

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        pass

class UserView(generic.TemplateView):
    template_name = 'home/user.html'
    view_user = None

    @method_decorator(login_required)
    def get(self, request, user_id=0):
        if user_id > 0:
            self.view_user = get_object_or_404(User, pk=user_id)

        return render(request, self.template_name,
            {'next': next, 'view_user': self.view_user}
        )

    @login_required()
    def userLogout(request):
        if request.user.is_authenticated:
            logout(request)
            return HttpResponseRedirect(reverse('home:index'))
        else:
            return HttpResponse('user error')

class UserLoginView(generic.TemplateView):
    template_name = 'home/login.html'
    form = None
    error_string = ''

    def get(self, request, page='login', next=''):
        if 'next' in request.GET:
            next = request.GET['next']

        if request.user.is_authenticated:
            if next != '':
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect(reverse('home:index'))

        if page == 'signup':
            self.form = RegisterForm()
        else:
            self.form = LoginForm()

        return render(request, self.template_name,
            {'next': next, 'form': self.form, 'page': page}
        )

    def post(self, request, next='', page='login', user=None):
        if 'next' in request.POST:
            next = request.POST['next']

        if page == 'signup':
            self.form = RegisterForm(request.POST)
            if self.form.is_valid():
                return HttpResponse('user valid')
            else:
                return HttpResponse('user error')

        else:
            self.form = LoginForm(request.POST)
            if self.form.is_valid():
                user = authenticate(username=self.form.cleaned_data['username'],
                    password= self.form.cleaned_data['password']
                )
                if user is not None:
                    login(request, user)
                    if next is not '':
                        return HttpResponseRedirect(next)
                    else:
                        return HttpResponseRedirect(reverse('home:index'))
                else:
                    self.error_string = "Your username and password didn't match. Please try again."

            return render(request, self.template_name,{
                'next': next,
                'form': self.form,
                'page': page,
                'error_string': self.error_string
            })
