from rest_framework import permissions


class OnlyPostAuthUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST','GET'] and bool(request.user and request.user.is_authenticated):
            return True
        return False
