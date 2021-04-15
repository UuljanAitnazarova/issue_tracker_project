from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.db.models import Q

from tracker.models import Issue, Status, Type, Project
from tracker.forms import IssueForm, SearchForm


class IndexView(LoginRequiredMixin,ListView):
    template_name = 'issue/index.html'
    model = Issue
    context_object_name = 'issues'
    ordering = ('summary', '-created_at')
    paginate_by = 2
    paginate_orphans = 1

    def get(self, request, **kwargs):
        self.form = SearchForm(request.GET)
        self.search_data = self.get_search_data()
        return super(IndexView, self).get(request, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.search_data:
            queryset = queryset.filter(
                Q(summary__icontains=self.search_data) |
                Q(description__icontains=self.search_data)
            )
        return queryset

    def get_search_data(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search_value']
        return None


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form
        return context


class IssueDetailView(LoginRequiredMixin, DetailView):
    template_name = 'issue/detail.html'
    model = Issue
    pk_url_kwarg = 'issue_pk'


class IssueCreateView(PermissionRequiredMixin,  CreateView):
    model = Issue
    template_name = 'issue/create.html'
    form_class = IssueForm
    permission_required = 'tracker.add_issue'

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        issue = form.save(commit=False)
        issue.project = project
        issue.save()
        form.save_m2m()
        return redirect(reverse('detail_view', kwargs={'issue_pk': issue.pk}))

    def has_permission(self):
        return super().has_permission() and self.request.user in Project.objects.get(pk=self.kwargs.get('pk')).user.all()




class IssueUpdateView(PermissionRequiredMixin, UpdateView):
    model = Issue
    template_name = 'issue/update.html'
    form_class = IssueForm
    context_object_name = 'issue'
    pk_url_kwarg = 'issue_pk'
    permission_required = 'tracker.change_issue'

    def get_success_url(self):
        return reverse('detail_view', kwargs={'issue_pk': self.object.pk})

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().project.user.all()



class IssueDeleteView(PermissionRequiredMixin, DeleteView):
    model = Issue
    template_name = 'issue/delete.html'
    context_object_name = 'issue'
    pk_url_kwarg = 'issue_pk'
    permission_required = 'tracker.delete_issue'

    def get_success_url(self):
        return reverse('detail_project', kwargs={'project_pk': self.object.project.pk})

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().project.user.all()
