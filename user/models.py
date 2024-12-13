from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email, username, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

# Role Model
class Role(models.Model):
    name = models.CharField(max_length=40, unique=True)
    
    def __str__(self):
        return self.name

# Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    role = models.OneToOneField(Role, on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Required for admin access
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'  # The field that will be used as the unique identifier (email in this case)
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']  # Fields required for creating a user

    objects = CustomUserManager()

    def __str__(self):
        return self.username

class Permission(models.Model):
    name = models.CharField(max_length=50)
    resource = models.CharField(max_length=100)
    role = models.ForeignKey(Role, related_name='permissions', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('role', 'resource')

    def __str__(self):
        return f"{self.name} - {self.resource}"

# AuditLog Model
class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('logout', 'Logout'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    resource = models.CharField(max_length=100)
    success = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} on {self.resource}"
