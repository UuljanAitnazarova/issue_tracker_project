from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse

from tracker.models import Project, Issue
from tracker.forms import ProjectForm

class MainView(ListView):
    template_name = 'project/mainpage.html'
    context_object_name = 'projects'
    model = Project
    paginate_by = 2
    paginate_orphans = 1


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project/detail.html'
    pk_url_kwarg = 'project_pk'

# class ProjectIssuesView


class ProjectCreateView(CreateView):
    template_name = 'project/create.html'
    form_class = ProjectForm
    model = Project



    def get_success_url(self):
        return reverse('main_page')


class ProjectUpdateView(UpdateView):
    model = Project
    template_name = 'project/update.html'
    form_class = ProjectForm
    context_object_name = 'project'
    pk_url_kwarg = 'project_pk'

    def get_success_url(self):
        return reverse('detail_project', kwargs={'project_pk': self.object.pk})


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'project/delete.html'
    pk_url_kwarg = 'project_pk'

    def get_success_url(self):
        return reverse('main_page')

