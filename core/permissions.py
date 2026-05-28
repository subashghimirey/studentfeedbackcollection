# core/permissions.py (or users/permissions.py)
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Allow anyone to view (GET, HEAD, OPTIONS).
    Restrict modifications (POST, PUT, PATCH, DELETE) to Superusers and 'admin' user_type.
    """
    def has_permission(self, request, view):
        # Allow read-only actions for everyone (or you could change this to request.user.is_authenticated)
        if request.method in SAFE_METHODS:
            return True
        
        # Check if the user is logged in and is either a superuser or has user_type == 'admin'
        return bool(request.user and request.user.is_authenticated and (
            request.user.is_superuser or getattr(request.user, 'user_type', None) == 'admin'
        ))

class IsAdminUserAction(BasePermission):
    """
    Strictly require Superuser or 'admin' user_type for any action.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (
            request.user.is_superuser or getattr(request.user, 'user_type', None) == 'admin'
        ))