from rest_framework import serializers
from .models import Employee
from django.contrib.auth import get_user_model

User = get_user_model()

class EmployeeRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'department', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            department=validated_data['department'],
            password=validated_data['password'],
        )
        return user


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Employee model with custom validations.
    """

    class Meta:
        model = Employee
        fields = ['id', 'email', 'first_name', 'last_name', 'department', 'is_supervisor', 'joining_date', 'is_active', 'is_staff']
        read_only = ['joined_date']
        extra_kwargs = {
            'email': {'validators': []},  # Remove default unique validator to add custom validation
            'password': {'write_only': True, 'min_length': 8},
            'is_active': {'read_only': True},
            'is_staff': {'read_only': True},
        }

    def validate_email(self, value):
        """
        Validate that the email is unique and properly formatted.
        """
        if Employee.objects.filter(email=value).exists():
            raise serializers.ValidationError("An employee with this email already exists.")
        return value

    def validate_first_name(self, value):
        """
        Validate that the first name contains only alphabetic characters.
        """
        if not value.isalpha():
            raise serializers.ValidationError("First name should contain only alphabetic characters.")
        return value

    def validate_last_name(self, value):
        """
        Validate that the last name contains only alphabetic characters.
        """
        if not value.isalpha():
            raise serializers.ValidationError("Last name should contain only alphabetic characters.")
        return value

    def validate_department(self, value):
        """
        Validate that the department name is not empty.
        """
        if not value.strip():
            raise serializers.ValidationError("Department name cannot be empty.")
        return value

    def create(self, validated_data):
        """
        Create and return a new Employee instance, setting the password properly.
        """
        password = validated_data.pop('password', None)
        employee = self.Meta.model(**validated_data)
        if password:
            employee.set_password(password)
        employee.save()
        return employee

    def update(self, instance, validated_data):
        """
        Update and return an existing Employee instance, setting the password properly if provided.
        """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
