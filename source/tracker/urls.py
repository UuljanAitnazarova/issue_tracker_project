from django.urls import path

from tracker.views import (
                IndexView,
                IssueDetailView,
                IssueCreateView,
                IssueUpdateView,
                IssueDeleteView,
                MainView,
                ProjectDetailView,
                ProjectCreateView,
)


urlpatterns = [
    path('', MainView.as_view(), name='main_page'),
    path('<int:project_pk>/', ProjectDetailView.as_view(), name='detail_project'),
    path('create/', ProjectCreateView.as_view(), name='create_project'),
    path('issues/', IndexView.as_view(), name='index_view'),
    path('issues/<int:issue_pk>/', IssueDetailView.as_view(), name='detail_view'),
    path('<int:pk>/issues/create/', IssueCreateView.as_view(), name='create_issue'),
    path('issues/<int:issue_pk>/update/', IssueUpdateView.as_view(), name='update_issue'),
    path('issues/<int:issue_pk>/delete/', IssueDeleteView.as_view(), name='delete_issue'),
]