from django.urls import path

from tracker.views import (
                IndexView,
                IssueDetailView,
                IssueCreateView,
                IssueUpdateView,
                IssueDeleteView,
                MainView,
                ProjectCreateView,
                ProjectUpdateView,
                ProjectDeleteView,
                ProjectIssuesView,
                ProjectUsersUpdateView,
)


urlpatterns = [
    path('', MainView.as_view(), name='main_page'),
    path('<int:project_pk>/', ProjectIssuesView.as_view(), name='detail_project'),
    path('<int:project_pk>/update', ProjectUpdateView.as_view(), name='update_project'),
    path('<int:project_pk>/delete', ProjectDeleteView.as_view(), name='delete_project'),
    path('create/', ProjectCreateView.as_view(), name='create_project'),
    path('<int:project_pk>/users/update', ProjectUsersUpdateView.as_view(), name='update_users'),
    path('issues/', IndexView.as_view(), name='index_view'),
    path('issues/<int:issue_pk>/', IssueDetailView.as_view(), name='detail_view'),
    path('<int:pk>/issues/create/', IssueCreateView.as_view(), name='create_issue'),
    path('issues/<int:issue_pk>/update/', IssueUpdateView.as_view(), name='update_issue'),
    path('issues/<int:issue_pk>/delete/', IssueDeleteView.as_view(), name='delete_issue'),
]