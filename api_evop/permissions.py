from rest_framework import permissions


class OnlyPostAuthUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST'] and bool(request.user and request.user.is_authenticated):
            return True
        return False


class IsAdminOrAuthPostOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST'] and bool(request.user and request.user.is_authenticated):
            return True
        elif request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)

