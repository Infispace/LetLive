"""
:synopsis: Used to define the views to manage users
"""
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
    #: The html template to render.
    template_name = 'home/topics.html'
    #: The topic to view, edit or delete.
    topic = None
    #: The Topic list.
    topic_list = None
    #: The Topic edit form.
    topic_form = None
    #: The error to be displayed.
    error_string = ''

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
        """
        Display topic list, topic form or the topic itself.
        Determined by the `page` context
        
        Shows A specific topic filtered with `/pk/`.
        
        :param request: the django HttpRequest object
        :type request: django.http.request.HttpRequest
        :param int topic_id: the topic id to filter
        """
        # get page context
        context = self.get_context_data()
        page = context['page']

        # get topic by id
        if topic_id != 0:
            self.topic = get_object_or_404(Topic, pk=topic_id)

        # get topic form
        if page == 'topic_new':
            self.topic_form = TopicForm() 
        elif page == 'topic_edit':
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
        """
        Creates a new topic.
        Edits or deletes a specific topic filtered with `/pk/`
        
        :param request: the django HttpRequest object
        :type request: django.http.request.HttpRequest
        :param int topic_id: the topic id to filter
        """
        # get page context
        context = self.get_context_data()
        page = context['page']
        
        # restrict to new, edit and delete
        permited = False;
        if page == 'topic_new' or page == 'topic_edit' or page == 'topic_delete':
            permited = True;

        if not permited:
            raise PermissionDenied

        # get topic by id
        if topic_id != 0:
            self.topic = get_object_or_404(Topic, pk=topic_id)

        # get topic form
        if page == 'topic_new':
            self.topic_form = TopicForm(request.POST)
        elif page == 'topic_edit':
            self.topic_form = TopicForm(request.POST, instance=self.topic)
        elif page == 'topic_delete':
            self.topic_form = TopicDeleteForm(request.POST, instance=self.topic)

        # make db changes
        success = False
        if self.topic_form.is_valid():
            try:
                if page == 'topic_new' or page == 'topic_edit':
                    self.topic_form.save()
                elif page == 'topic_delete':
                    self.topic.delete()
                    
                success = True
            except Exception as e:
                success = False
                self.error_string = 'There was an error. Please try again.' 
                if settings.DEBUG:
                    self.error_string = e
        
        # render template
        if success:
            return HttpResponseRedirect(reverse('home:topic_default'))
        else:
            return self.render_to_response({
                'page':page,
                'topic': self.topic,
                'topic_list': self.topic_list,
                'topic_form': self.topic_form,
                'error_string': self.error_string
            })

