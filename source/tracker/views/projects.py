from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from tracker.models import Project, Issue
from tracker.forms import ProjectForm


class MainView(ListView):
    template_name = 'project/mainpage.html'
    context_object_name = 'projects'
    model = Project
    paginate_by = 2
    paginate_orphans = 1


class ProjectIssuesView(ListView):
    template_name = 'project/detail.html'
    paginate_by = 2
    paginate_orphans = 1
    context_object_name = 'issues'

    def get_queryset(self):
        self.project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        return Issue.objects.filter(project=self.project)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.project
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    template_name = 'project/create.html'
    form_class = ProjectForm
    model = Project


    def get_success_url(self):
        return reverse('main_page')


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    template_name = 'project/update.html'
    form_class = ProjectForm
    context_object_name = 'project'
    pk_url_kwarg = 'project_pk'

    def get_success_url(self):
        return reverse('detail_project', kwargs={'project_pk': self.object.pk})


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'project/delete.html'
    pk_url_kwarg = 'project_pk'

    def get_success_url(self):
        return reverse('main_page')

