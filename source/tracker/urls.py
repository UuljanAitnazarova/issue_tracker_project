from django.urls import path

from .views import IndexView, IssueDetailView

urlpatterns = [
    path('', IndexView.as_view(), name='index_view'),
    path('<int:issue_pk>/', IssueDetailView.as_view(), name='detail_view'),
]