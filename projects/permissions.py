from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .models import Contributor


class IsContributor(permissions.BasePermission):
    """
    Custom permission to only allow contributors of a project
    to create or retrieve issues.
    """
    def has_permission(self, request, view):
        project_id = view.kwargs.get('project_id')
        return Contributor.objects.filter(user=request.user, project_id=project_id).exists()


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the author of an issue
    to edit or delete it. Others can only read.
    """
    
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

