from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
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

    def get(self, request, topic_id):
        return HttpResponse('topic view')

class ArticleView(generic.DetailView):
    model = Article
    template_name = 'home/article.html'

    def get(self, request, article_id):
        return HttpResponse('article view')

class UserView(generic.DetailView):
    model = Author
    template_name = 'home/user.html'

    def get(self, request, user_id):
        return HttpResponse('user view')
