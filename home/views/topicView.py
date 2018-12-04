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

from ..models.topicModel import Topic

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
