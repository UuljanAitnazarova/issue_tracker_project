from django.urls import path

from .views import IndexView, IssueDetailView, IssueCreateView, IssueUpdateView, IssueDeleteView

urlpatterns = [
    path('', IndexView.as_view(), name='index_view'),
    path('<int:issue_pk>/', IssueDetailView.as_view(), name='detail_view'),
    path('create/', IssueCreateView.as_view(), name='create_issue'),
    path('<int:issue_pk>/update/', IssueUpdateView.as_view(), name='update_issue'),
    path('<int:issue_pk>/delete/', IssueDeleteView.as_view(), name='delete_issue'),
]