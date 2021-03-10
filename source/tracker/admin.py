from django.contrib import admin

from tracker.models import Issue, Status, Type

admin.site.register(Issue)
admin.site.register(Status)
admin.site.register(Type)
