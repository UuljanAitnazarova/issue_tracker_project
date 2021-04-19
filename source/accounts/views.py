from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect, reverse
from django.views.generic import CreateView
from django.views.generic import DetailView, ListView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator

from accounts.forms import MyUserCreationForm


class RegisterView(CreateView):
    model = User
    template_name = 'registration/register.html'
    form_class = MyUserCreationForm
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        print(next_url, '1')
        if not next_url:
            next_url = self.request.POST.get('next')
            print(next_url, '2')
        if not next_url:
            next_url = reverse('main_page')
            print(next_url, '3')
        return next_url



class UserDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'
    paginate_related_by = 5
    paginate_related_orphans = 0

    def get_context_data(self, **kwargs):
        projects = self.object.projects.all().order_by('-start_date')
        paginator = Paginator(projects, self.paginate_related_by, orphans=self.paginate_related_orphans)
        page_number = self.request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        kwargs['page_obj'] = page
        kwargs['projects'] = page.object_list
        kwargs['is_paginated'] = page.has_other_pages()
        return super().get_context_data(**kwargs)


class UsersListView(PermissionRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'users_list.html'
    context_object_name = 'users'
    permission_required = 'tracker.users_view'