from django.shortcuts import render
from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import EmployeeSerializer, CustomerSerializer, TasklistSerializer, TaskSerializer
from .permissions import IsEmployee, IsFullAccessEmployee, IsCustomer, IsCustomerOrEmployee
from .models import Task
from django.http import Http404


User = get_user_model()


class EmployeeApiView(generics.ListCreateAPIView):
    queryset = User.objects.filter(role=2)
    serializer_class = EmployeeSerializer
    permission_classes = [IsCustomerOrEmployee]

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsFullAccessEmployee]
        return super().get_permissions()


class CustomerApiView(generics.ListCreateAPIView):
    queryset = User.objects.filter(role_id=1)
    serializer_class = CustomerSerializer
    permission_classes = [IsEmployee]

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsFullAccessEmployee]
        return super().get_permissions()


class TasklistApiView(generics.ListCreateAPIView):
    serializer_class = TasklistSerializer
    permission_classes = [IsCustomerOrEmployee]

    def get_queryset(self):
        user = self.request.user

        if user.role.name == 'customer':
            return Task.objects.filter(customer=user)
        elif user.role.name == 'employee' and not user.full_access:
            return Task.objects.filter(Q(employee=user) | Q(employee__isnull=True))
        elif user.role.name == 'employee' and user.full_access:
            return Task.objects.all()
        else:
            return Task.objects.none()

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsCustomer]
        return super().get_permissions()


class TakeTaskApiView(generics.UpdateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsEmployee]

    def get_queryset(self):
        return Task.objects.filter(employee_id=None)

    def patch(self, request, *args, **kwargs):
        try:
            task = self.get_object()
        except Http404:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        task.employee_id = request.user.id
        task.status = 'in_progress'
        task.save()
        return Response(self.get_serializer(task).data, status=status.HTTP_200_OK)


class FinishTaskApiView(generics.UpdateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.all()

    def patch(self, request, *args, **kwargs):
        try:
            task = self.get_object()
        except Http404:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        if task.employee_id != request.user.id:
            return Response({'error': 'You do not have permission to complete this task'}, status=status.HTTP_403_FORBIDDEN)

        if task.status == 'completed':
            return Response({'error': 'This task is already completed and cannot be edited'},
                            status=status.HTTP_400_BAD_REQUEST)

        task.status = 'completed'
        report = request.data.get('report', '')
        task.report = report
        task.save()
        return Response(self.get_serializer(task).data, status=status.HTTP_200_OK)
