from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.views.generic import TemplateView

from ..models import Topic
from ..forms import TopicForm, TopicDeleteForm

class TopicView(TemplateView):
    template_name = 'home/topic.html'
    topic = None
    topic_list = None
    topic_form = TopicForm()

    def new_topic(self, user):
        if(not user.has_perm('home.add_topic')):
            raise PermissionDenied

    def edit_topic(self, user):
        if(not user.has_perm('home.change_topic')):
            raise PermissionDenied

    def delete_topic(self, user):
        if(not user.has_perm('home.delete_topic')):
            raise PermissionDenied

    def get(self, request, topic_id=0, page='topic'):
        if topic_id != 0:
            self.topic = get_object_or_404(Topic, pk=topic_id)

        if page == 'topic_edit':
            self.edit_topic(request.user)
            self.topic_form = TopicForm(instance=self.topic)
        elif page == 'topic_new':
            self.new_topic(request.user)
        elif page == 'topic_default':
            self.topic_list = Topic.objects.all()
        elif page == 'topic_delete':
            self.delete_topic(request.user)
            self.topic_form = TopicDeleteForm(instance=self.topic)

        return render(request, self.template_name, {
            'page':page,
            'topic': self.topic,
            'topic_list': self.topic_list,
            'topic_form': self.topic_form
        })

    def post(self, request, topic_id=0, page='topic'):
        if topic_id != 0:
            self.topic = get_object_or_404(Topic, pk=topic_id)

        error_string = None
        if page == 'topic_edit':
            self.edit_topic(request.user)
            self.topic_form = TopicForm(request.POST, instance=self.topic)
        elif page == 'topic_new':
            self.new_topic(request.user)
            self.topic_form = TopicForm(request.POST)
        elif page == 'topic_delete':
            self.delete_topic(request.user)
            self.topic_form = TopicDeleteForm(request.POST, instance=self.topic)
            if self.topic_form.is_valid():
                self.topic = get_object_or_404(
                    Topic,
                    topic_name=self.topic_form.cleaned_data['topic_name']
                )
                self.topic.delete()
                return HttpResponseRedirect(reverse('home:topic_default'))
            else:
                return render(request, self.template_name, {
                    'page': page,
                    'user_delete': user_delete,
                    'form': user_delete_form,
                    'error_string': error_string,
                })


        if self.topic_form.is_valid():
            self.topic_form.save()
            return HttpResponseRedirect(reverse('home:topic_default'))
        else:
            error_string = 'Check the following form errors!'

        return render(request, self.template_name, {
            'page':page,
            'topic': self.topic,
            'topic_list': self.topic_list,
            'topic_form': self.topic_form,
            'error_string': error_string
        })
