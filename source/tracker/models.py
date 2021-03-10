from django.db import models

class Issue(models.Model):
    summary = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(max_length=1000, blank=True, null=True)
    status = models.ForeignKey('tracker.Status', on_delete=models.PROTECT)
    type = models.ForeignKey('tracker.Type', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Status(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)

class Type(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)