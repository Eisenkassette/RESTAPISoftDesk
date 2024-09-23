from rest_framework import permissions


class IsAuthenticatedOrCreateOnly(permissions.BasePermission):
    '''
    Enforces user authentications except for the POST method
    '''
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user.is_authenticated


class IsAuthorOrReadOnly(permissions.BasePermission):
    '''
    Check if the user is authenticated.
    For specfic objects, allow GET but check if the user is the author for all other methods.
    '''
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return obj == request.user
