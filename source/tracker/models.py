from django.db import models

from tracker.validators import validate_integers, SpecialSymbolsValidator


class Issue(models.Model):
    summary = models.CharField(max_length=200, blank=False, null=False, validators=[validate_integers])
    description = models.TextField(max_length=1000, blank=True, null=True, validators=[SpecialSymbolsValidator(['@', '#', '$', '&', '%'])])
    status = models.ForeignKey('tracker.Status', on_delete=models.PROTECT, related_name='issues')
    type = models.ManyToManyField('tracker.Type', related_name='issues')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project = models.ForeignKey('tracker.Project', related_name='issues', on_delete=models.CASCADE)

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



class Project(models.Model):
    name = models.CharField(max_length=300, blank=False, null=False)
    description = models.TextField(max_length=1000, blank=False, null=False)
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=True, null=True)
    user = models.ManyToManyField('auth.User', related_name='projects')

    def __str__(self):
        return f'{self.pk},{self.description}'

    class Meta:
        permissions = [
            ('can_update_users_in_project', 'Can update users in project')
        ]
