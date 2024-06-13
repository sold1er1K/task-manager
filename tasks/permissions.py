from rest_framework import permissions


class BaseRolePermission(permissions.BasePermission):
    required_roles = []
    full_access_required = False

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.role.name not in self.required_roles:
            return False
        if self.full_access_required and not user.full_access:
            return False
        return True


class IsEmployee(BaseRolePermission):
    required_roles = ['employee']


class IsFullAccessEmployee(BaseRolePermission):
    required_roles = ['employee']
    full_access_required = True


class IsCustomer(BaseRolePermission):
    required_roles = ['customer']


class IsCustomerOrEmployee(BaseRolePermission):
    required_roles = ['customer', 'employee']
