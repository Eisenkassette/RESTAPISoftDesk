from django.contrib import admin
from .models import Project, Contributor, Issues, Comment

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'author', 'creation_date')
    list_filter = ('type', 'creation_date')
    search_fields = ('title', 'description')

@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'creation_date')
    list_filter = ('project', 'creation_date')
    search_fields = ('user__username', 'project__title')

@admin.register(Issues)
class IssuesAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'priority', 'type', 'status', 'author', 'creation_date')
    list_filter = ('priority', 'type', 'status', 'project', 'creation_date')
    search_fields = ('name', 'description', 'project__name', 'author__username')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'issue', 'author', 'creation_date')
    list_filter = ('project', 'issue', 'creation_date')
    search_fields = ('description', 'author__username', 'project__title', 'issue__name')