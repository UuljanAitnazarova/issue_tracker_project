from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


from tracker.models import Project, Issue
from tracker.forms import ProjectForm, ProjectUserForm


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


class ProjectCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'project/create.html'
    form_class = ProjectForm
    model = Project
    permission_required = 'tracker.add_project'

    def form_valid(self, form):
        # print(self.request.user.pk)
        project = form.save()
        project.user.add(self.request.user)
        return super().form_valid(form)


    def get_success_url(self):

        return reverse('main_page')


class ProjectUpdateView(PermissionRequiredMixin, UpdateView):
    model = Project
    template_name = 'project/update.html'
    form_class = ProjectForm
    context_object_name = 'project'
    pk_url_kwarg = 'project_pk'
    permission_required = 'tracker.change_project'

    def get_success_url(self):
        return reverse('detail_project', kwargs={'project_pk': self.object.pk})


class ProjectDeleteView(PermissionRequiredMixin, DeleteView):
    model = Project
    template_name = 'project/delete.html'
    pk_url_kwarg = 'project_pk'
    permission_required = 'tracker.delete_project'

    def get_success_url(self):
        return reverse('main_page')


class ProjectUsersUpdateView(PermissionRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectUserForm
    template_name = 'user/update.html'
    pk_url_kwarg = 'project_pk'
    permission_required = 'tracker.can_update_users_in_project'


    def get_success_url(self):
        return reverse('detail_project', kwargs={'project_pk': self.object.pk})

    # def has_permission(self):
    #     return super().has_permission() and self.request.user in self.get_object().user.all()

