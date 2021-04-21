from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.models import User
from django.shortcuts import redirect, reverse
from django.views.generic import CreateView, UpdateView
from django.views.generic import DetailView, ListView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator

from accounts.forms import MyUserCreationForm, UserUpdateForm, ProfileUpdateForm, PasswordChangeForm
from accounts.models import Profile


class RegisterView(CreateView):
    model = User
    template_name = 'registration/register.html'
    form_class = MyUserCreationForm
    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
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


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'user_update.html'
    form_class = UserUpdateForm
    context_object_name = 'user_obj'

    profile_form_class = ProfileUpdateForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_form = self.get_form()
        profile_form = self.get_profile_form()

        if user_form.is_valid() and profile_form.is_valid():
            return self.form_valid(user_form, profile_form)
        return self.form_invalid(user_form, profile_form)

    def get_object(self, queryset=None):
        return self.request.user

    def get_profile_form(self):
        form_kwargs = {'instance': self.object.profile}

        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return self.profile_form_class(**form_kwargs)

    def form_valid(self, user_form, profile_form):
        response = super(UserUpdateView, self).form_valid(user_form)
        profile_form.save()
        return response

    def form_invalid(self, user_form, profile_form):
        context = self.get_context_data(
            form=user_form,
            profile_form=profile_form
        )
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['profile_form'] = kwargs.get('profile_form')
        if context['profile_form'] is None:
            context['profile_form'] = self.get_profile_form()
        return context

    def get_success_url(self):
        return reverse('accounts:detail', kwargs={'pk': self.object.pk})





class UserPasswordChangeView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'user_password_change.html'
    form_class = PasswordChangeForm
    context_object_name = 'user_obj'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super(UserPasswordChangeView, self).form_valid(form)
        update_session_auth_hash(self.request, self.request.user)
        return response

    def get_success_url(self):
        return reverse('accounts:detail', kwargs={'pk': self.object.pk})





