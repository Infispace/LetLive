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
