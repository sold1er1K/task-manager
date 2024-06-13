from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Role


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'father_name', 'email', 'phone', 'full_access')
        extra_kwargs = {
            'username': {'write_only': True},
            'password': {'write_only': True},
            'full_access': {'write_only': True},
        }

    def create_user_with_role(self, validated_data, role_name, full_access):
        role = Role.objects.get(name=role_name)
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            father_name=validated_data['father_name'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            role=role,
            full_access=full_access
        )
        return user

    def create(self, validated_data):
        raise NotImplementedError("Use EmployeeSerializer or CustomerSerializer to create a user.")


class EmployeeSerializer(UserSerializer):
    def create(self, validated_data):
        full_access = validated_data.get('full_access', False)
        return self.create_user_with_role(validated_data, 'employee', full_access)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['full_access'] = instance.full_access
        return representation


class CustomerSerializer(UserSerializer):
    def create(self, validated_data):
        return self.create_user_with_role(validated_data, 'customer', False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if 'full_access' in representation:
            representation.pop('full_access')
        return representation
