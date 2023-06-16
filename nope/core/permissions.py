from rest_framework.permissions import BasePermission


class AuthOrOptions(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True
        if request.META.get('PATH_INFO') == '/api/':
            return True
        return bool(request.user and request.user.is_authenticated)
