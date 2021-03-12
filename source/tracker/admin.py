from django.contrib import admin

from tracker.models import Issue, Status, Type

class IssueAdmin(admin.ModelAdmin):
    list_display = ['id', 'summary', 'description', 'status']
    list_filter = ['status', 'type']
    search_fields = ['summary']
    fields = ['summary', 'description', 'status', 'type']


admin.site.register(Issue, IssueAdmin)
admin.site.register(Status)
admin.site.register(Type)
