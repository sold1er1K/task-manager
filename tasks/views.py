from django.shortcuts import render
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import EmployeeSerializer, CustomerSerializer
from .permissions import IsEmployee, IsFullAccessEmployee, IsCustomer, IsCustomerOrEmployee


User = get_user_model()


class EmployeeApiView(generics.ListCreateAPIView):
    queryset = User.objects.filter(role=2)
    serializer_class = EmployeeSerializer
    permission_classes = [IsCustomerOrEmployee]


class CustomerApiView(generics.ListCreateAPIView):
    queryset = User.objects.filter(role_id=1)
    serializer_class = CustomerSerializer
    permission_classes = [IsEmployee]

