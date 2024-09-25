from rest_framework import permissions
from .models import Contributor


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

class IsAuthorOrContributorReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow:
    - Contributors to read the object
    - Author to modify or delete the object
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        project_id = view.kwargs.get('project_id')
        return Contributor.objects.filter(user=request.user, project_id=project_id).exists()

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
