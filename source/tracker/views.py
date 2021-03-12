from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateView
from django.views import View

from tracker.models import Issue, Status, Type
from tracker.forms import IssueForm


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        print(kwargs)
        context = super().get_context_data(**kwargs)
        context['issues'] = Issue.objects.all()
        return context


class IssueDetailView(TemplateView):
    template_name = 'issue_detail.html'

    def get_context_data(self, **kwargs):
        print(kwargs)
        context = super().get_context_data(**kwargs)

        context['issue'] = get_object_or_404(Issue, pk=kwargs['issue_pk'])
        print(context)
        return context


class IssueCreateView(View):

    def get(self, request, *args, **kwargs):
        form = IssueForm()
        return render(request, 'issue_create.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = IssueForm(data=request.POST)

        if form.is_valid():
            type = form.cleaned_data.pop('type')
            issue = Issue.objects.create(**form.cleaned_data)
            issue.type.set(type)
            return redirect('detail_view', issue_pk=issue.pk)
        return render(request, 'issue_create.html', context={'form': form})


class IssueUpdateView(View):

    def get(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, id=kwargs.get('issue_pk'))
        form = IssueForm(initial={
            'summary': issue.summary,
            'description': issue.description,
            'typ': issue.type,
            'status': issue.status,
        })
        return render(request, 'issue_update.html', context={'form': form, 'issue': issue})

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
        return render(request, 'issue_update.html', context={'form': form, 'issue': issue})


class IssueDeleteView(View):

    def get(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, id=kwargs.get('issue_pk'))
        return render(request, 'issue_delete.html', context={'issue': issue})

    def post(self, request, *args, **kwargs):
        issue = get_object_or_404(Issue, id=kwargs.get('issue_pk'))
        issue.delete()
        return redirect('index_view')
