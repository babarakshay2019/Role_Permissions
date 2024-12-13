from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RoleViewSet, PermissionViewSet, AuditLogViewSet,RegisterView,UserRoleAssignmentViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'permissions', PermissionViewSet, basename='permission')
router.register(r'audit-logs', AuditLogViewSet, basename='audit-log')
router.register(r'assign-role', UserRoleAssignmentViewSet, basename='assign-role')


urlpatterns = [
      # This will include all the registered routes
]

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    # path('assign_role/',UserRoleAssignmentViewSet.as_view(),name='assign_role'),
    path('', include(router.urls)),
]