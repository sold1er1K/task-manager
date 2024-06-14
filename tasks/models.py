from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    father_name = models.CharField(max_length=20, verbose_name='Отчество')
    phone = models.CharField(max_length=15, unique=True, verbose_name='Телефон')
    full_access = models.BooleanField(default=False, verbose_name='Полный доступ', blank=True)
    role = models.ForeignKey('Role', on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.father_name}"


class Role(models.Model):
    name = models.CharField(max_length=20, db_index=False)

    def __str__(self):
        return self.name


class Task(models.Model):
    TASK_STATUSES = [
        ("pending", "Ожидает исполнителя"),
        ("in_progress", "Выполняется"),
        ("completed", "Выполнена"),
    ]

    customer = models.ForeignKey(User, related_name='customer_tasks', on_delete=models.CASCADE,
                                 limit_choices_to={'role__name': 'customer'}, null=True)
    employee = models.ForeignKey(User, related_name='employee_tasks', on_delete=models.CASCADE,
                                 limit_choices_to={'role__name': 'employee'}, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    description = models.TextField(blank=True)
    report = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=TASK_STATUSES, default='pending')

    def save(self, *args, **kwargs):
        if self.status == 'completed' and not self.report:
            raise ValueError("Отчет не может быть пустым при закрытии задачи.")
        if self.status == 'completed' and not self.closed_at:
            self.closed_at = timezone.now()
        super().save(*args, **kwargs)
