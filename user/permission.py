from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow access to users with the admin role.
    """
    def has_permission(self, request, view):
        print(request.user.role)

        return request.user.is_authenticated and request.user.role.name == 'admin'


class IsAdminOrSupervisor(permissions.BasePermission):
    """
    Custom permission to only allow access to users with the admin role.
    """
    def has_permission(self, request, view):
        print(request.user.role)
    
        return request.user.is_authenticated and (request.user.role.name == 'admin' or request.user.role.name == 'supervisor')