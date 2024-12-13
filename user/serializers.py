from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Role,Permission, AuditLog

User = get_user_model()

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # role = RoleSerializer(read_only=True) # Include roles associated with the user

    class Meta:
        model = User
        fields = ['id', 'username', 'email','first_name', 'last_name','password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'resource', 'role']

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'action', 'resource', 'success', 'timestamp']
    

