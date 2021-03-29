from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import urlencode
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic import ListView, CreateView
from django.views import View
from django.db.models import Q


from tracker.models import Issue, Status, Type, Project
from tracker.forms import IssueForm, SearchForm


class IndexView(ListView):
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


class IssueDetailView(TemplateView):
    template_name = 'issue/detail.html'


    def get_context_data(self, **kwargs):
        print(kwargs)
        context = super().get_context_data(**kwargs)

        context['issue'] = get_object_or_404(Issue, pk=kwargs['issue_pk'])
        print(context)
        return context


class IssueCreateView(CreateView):
    model = Issue
    template_name = 'issue/create.html'
    form_class = IssueForm

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        issue = form.save(commit=False)
        issue.project = project
        issue.save()
        form.save_m2m()
        return redirect(reverse('detail_view', kwargs={'issue_pk': issue.pk}))




class IssueUpdateView(View):

    def get(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, id=kwargs.get('issue_pk'))
        form = IssueForm(initial={
            'summary': issue.summary,
            'description': issue.description,
            'type': issue.type.all(),
            'status': issue.status,
        })
        return render(request, 'issue/update.html', context={'form': form, 'issue': issue})

    def post(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, id=kwargs.get('issue_pk'))
        form = IssueForm(data=request.POST)
        if form.is_valid():
            issue.summary = form.cleaned_data.get('summary')
            issue.description = form.cleaned_data.get('description')
            issue.type.set(form.cleaned_data.get('type'))
            issue.status = form.cleaned_data.get('status')
            issue.save()
            return redirect('detail_view', issue_pk=issue.pk)
        return render(request, 'issue/issue_update.html', context={'form': form, 'issue': issue})


class IssueDeleteView(View):

    def get(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, id=kwargs.get('issue_pk'))
        return render(request, 'issue/delete.html', context={'issue': issue})

    def post(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, id=kwargs.get('issue_pk'))
        issue.delete()
        return redirect('index_view')
