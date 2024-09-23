from django.conf import settings
from django.utils import timezone
from django.db import models
import uuid


class Project(models.Model):
    title = models.CharField(max_length=75, unique=True)
    description = models.TextField(max_length=300, blank=True)

    type = models.CharField(max_length=9, choices=[('BACK-END', 'BACK-END'), 
                                                   ('FRONT-END', 'FRONT-END'), 
                                                   ('IOS', 'IOS'), 
                                                   ('ANDROID', 'ANDROID'),])

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authored_projects')
    contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Contributor', related_name='contributed_projects')

    creation_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            Contributor.objects.create(user=self.author, project=self)

    def __str__(self):
        return self.title


class Contributor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    creation_date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return f"{self.user} - {self.project.title}"


class Issues(models.Model):
    name = models.CharField(max_length=75)
    description = models.TextField(max_length=300, blank=True)

    priority = models.CharField(max_length=6, choices=[('LOW', 'LOW'), 
                                                       ('MEDIUM', 'MEDIUM'), 
                                                       ('HIGH', 'HIGH'),])
    
    type = models.CharField(max_length=7, choices=[('BUG', 'BUG'), 
                                                   ('FEATURE', 'FEATURE'), 
                                                   ('TASK', 'TASK'),])
    
    status = models.CharField(max_length=10, choices=[('TODO', 'TODO'), 
                                                      ('INPROGRESS', 'INPROGRESS'), 
                                                      ('FINISHED', 'FINISHED'),])
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authored_issues')
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='assigned_issues', blank=True)
    creation_date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('name', 'project')

    def __str__(self):
        return self.name


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='comments', null=True)
    issue = models.ForeignKey(Issues, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    description = models.TextField(max_length=300)
    creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.description[:100]}..."
