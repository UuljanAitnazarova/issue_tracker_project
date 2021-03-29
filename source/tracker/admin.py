from django.contrib import admin

from tracker.models import Issue, Status, Type, Project

class IssueAdmin(admin.ModelAdmin):
    list_display = ['id', 'summary', 'description', 'status']
    list_filter = ['status', 'type']
    search_fields = ['summary']
    fields = ['summary', 'description', 'status', 'type', 'project']


admin.site.register(Issue)
admin.site.register(Status)
admin.site.register(Type)
admin.site.register(Project)
