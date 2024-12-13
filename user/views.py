from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets, status, filters
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser,Permission,Role,AuditLog
from .serializers import UserSerializer,RoleSerializer,PermissionSerializer,AuditLogSerializer
from .permission import IsAdminUser,IsAdminOrSupervisor


User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAdminOrSupervisor])
    def assign_role(self, request, pk=None):
        """
        Update the role of a user. Only admin or supervisor users can update roles.
        """
        try:
            user = CustomUser.objects.get(id=pk)

            # Get the role from request data
            role_name = request.data.get('role')
            if not role_name:
                return Response({"error": "Role is required."}, status=400)

            # Get the Role object
            role = Role.objects.filter(name=role_name).first()
            if not role:
                return Response({"error": "Invalid role."}, status=400)

            # Update the user's role
            user.role = role
            user.save()

            return Response({"message": f"Role '{role_name}' updated successfully for {user.username}."})
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=404)



class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]  


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['role']


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]



class UserRoleAssignmentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def assign_role(self, request, pk=None):
        """
        Assign a single role to a user.
        """
        user = User.objects.get(id=pk)
        role_name = request.data.get('role')
        role = Role.objects.filter(name=role_name).first()

        if role:
            user.role = role  # Assign the role to the user
            user.save()
            return Response({"message": f"Role '{role_name}' assigned successfully."})
        
        return Response({"error": "Invalid role."}, status=400)

    # @action(detail=True, methods=['get'])
    # def get_role(self, request, pk=None):
    #     """
    #     Get the role assigned to a user.
    #     """
    #     user = User.objects.get(id=pk)
    #     role = user.role
    #     if role:
    #         return Response({"role": role.name})
    #     return Response({"role": "No role assigned"}, status=404)