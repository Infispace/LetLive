from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.urls import reverse
from django.views import generic

from ..forms import UserForm, AuthorForm, PublisherForm, AdminForm

class ProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'home/account.html'
    view_user = None
    form = None

    def set_form(self, user, request=None):
        try:
            user.author
            if request is not None:
                self.form = AuthorForm(request.POST, instance=user.author)
            else:
                self.form = AuthorForm(instance=user.author)
        except ObjectDoesNotExist:
            pass

        try:
            user.publisher
            if request is not None:
                self.form = PublisherForm(request.POST, instance=user.publisher)
            else:
                self.form = PublisherForm(instance=user.publisher)
        except ObjectDoesNotExist:
            pass

        try:
            user.admin
            if request is not None:
                self.form = AdminForm(request.POST, instance=user.admin)
            else:
                self.form = AdminForm(instance=user.admin)
        except ObjectDoesNotExist:
            pass

    def get(self, request, page, user_id=0):
        editable = False
        if user_id != 0:
            self.view_user = get_object_or_404(User, pk=user_id)
        else:
            editable = True
            self.view_user = request.user

        self.set_form(self.view_user)
        user_form = UserForm(instance=self.view_user)
        return render(request, self.template_name, {
            'view_user': self.view_user,
            'form_user': user_form,
            'form_profile': self.form,
            'editable': editable,
            'page': page
        })

    def post(self, request, page):
        user_form = UserForm(request.POST, instance=request.user)
        self.set_form(request.user, request)
        saved = False

        if user_form.has_changed():
            if user_form.is_valid():
                user_form.save()
                saved = True

        if self.form.has_changed():
            if self.form.is_valid():
                self.form.save()
                saved = True

        error_string = None
        if saved:
            return HttpResponseRedirect(reverse('home:user_default'))
        else:
            error_string = 'Check the following form errors!'

        return render(request, self.template_name, {
            'form_user': user_form,
            'form_profile': self.form,
            'editable': True,
            'error_string': error_string,
            'page': page
        })
