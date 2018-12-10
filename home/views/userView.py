from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.urls import reverse
from django.views import generic

from ..forms.userForm import UserForm, AuthorForm, PublisherForm, AdminForm

@login_required()
def userLogout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse('home:index'))
    else:
        return HttpResponse('Unknown Error')

class UserView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'home/user.html'
    view_user = None
    form = None

    def set_form(self, user):
        try:
            user.author
            self.form = AuthorForm(instance=user)
        except ObjectDoesNotExist:
            pass

        try:
            user.publisher
            self.form = PublisherForm(instance=user)
        except ObjectDoesNotExist:
            pass

        try:
            user.admin
            self.form = AdminForm(instance=user)
        except ObjectDoesNotExist:
            pass

    def get(self, request, user_id=0):
        editable = False
        if user_id != 0:
            self.view_user = get_object_or_404(User, pk=user_id)
        else:
            editable = True
            self.view_user = request.user

        self.set_form(self.view_user)
        user_form = UserForm(instance=self.view_user)
        return render(request, self.template_name, {
            'form_user': user_form,
            'form_profile': self.form,
            'editable': editable
        })

    def post(self, request):
        print('not saved')

        return HttpResponseRedirect(reverse('home:user_default'))
