from django.db import models

class Issue(models.Model):
    summary = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(max_length=1000, blank=True, null=True)
    status = models.ForeignKey('tracker.Status', on_delete=models.PROTECT, related_name='issues')
    type = models.ManyToManyField('tracker.Type', related_name='issues')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.summary


class Status(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return self.name

