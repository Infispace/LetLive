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

class UserView(generic.TemplateView):
    template_name = 'home/user.html'
    view_user = None

    @method_decorator(login_required)
    def get(self, request, user_id=0):
        if user_id > 0:
            self.view_user = get_object_or_404(User, pk=user_id)
        else:
            self.view_user = request.user

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
