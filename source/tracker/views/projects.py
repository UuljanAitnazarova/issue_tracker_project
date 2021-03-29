from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse

from tracker.models import Project
from tracker.forms import ProjectForm

class MainView(ListView):
    template_name = 'project/mainpage.html'
    context_object_name = 'projects'
    model = Project

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project/detail.html'
    pk_url_kwarg = 'project_pk'



class ProjectCreateView(CreateView):
    template_name = 'project/create.html'
    form_class = ProjectForm
    model = Project


    def get_success_url(self):
        return reverse('main_page')
