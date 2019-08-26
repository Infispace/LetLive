from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from home.models import Topic
from home.forms import TopicForm
from home.forms import TopicDeleteForm

class TopicView(PermissionRequiredMixin, TemplateView):
    template_name = 'home/topics.html'
    topic = None
    topic_list = None
    topic_form = TopicForm()

    def get_permission_required(self):
        permission_required = ''
        context = self.get_context_data()
        
        if context['page'] == 'topic_new':
            permission_required = ['home.add_topic']
        elif context['page'] == 'topic_edit':
            permission_required = ['home.change_topic']
        elif context['page'] == 'topic_delete':
            permission_required = ['home.delete_topic']
        
        return permission_required
    
    def get(self, request, topic_id=0, *args, **kwargs):
        # get page context
        context = self.get_context_data()
        page = context['page']
        
        # get topic by id
        if topic_id != 0:
            self.topic = get_object_or_404(Topic, pk=topic_id)

        # get topic form
        if page == 'topic_edit':
            self.topic_form = TopicForm(instance=self.topic) 
        elif page == 'topic_delete':
            self.topic_form = TopicDeleteForm(instance=self.topic)
            
        # get topic list
        if page == 'topic_default':
            self.topic_list = Topic.objects.all()
        
        return self.render_to_response({
            'page':page,
            'topic': self.topic,
            'topic_list': self.topic_list,
            'topic_form': self.topic_form
        })

    def post(self, request, topic_id=0, *args, **kwargs):
        # get page context
        context = self.get_context_data()
        page = context['page']
        
        # get topic by id
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
                return self.render_to_response({
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

        return self.render_to_response({
            'page':page,
            'topic': self.topic,
            'topic_list': self.topic_list,
            'topic_form': self.topic_form,
            'error_string': error_string
        })

