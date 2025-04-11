import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)


class EmployeeManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, department, password=None, **extra_fields):
        """
        Create and save an Employee with the given email, name, department, and password.
        """
        if not email:
            raise ValueError("Employees must have an email address")
        email = self.normalize_email(email)
        employee = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            department=department,
            **extra_fields
        )
        employee.set_password(password)
        employee.save(using=self._db)
        return employee

    def create_superuser(self, email, first_name, last_name, department, password=None, **extra_fields):
        """
        Create and save a superuser (admin) with the given email, name, department, and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_supervisor", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, first_name, last_name, department, password, **extra_fields)
    


class Employee(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for employees.
    Uses email as the unique identifier for authentication.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    is_supervisor = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    joining_date = models.DateField(default=timezone.now)

    objects = EmployeeManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "department"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
