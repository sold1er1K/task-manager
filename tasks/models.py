from django.contrib.auth.models import AbstractUser
from django.db import models


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
