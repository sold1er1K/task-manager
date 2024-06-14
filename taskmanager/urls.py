from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from tasks.views import EmployeeApiView, CustomerApiView, TasklistApiView, TakeTaskApiView, FinishTaskApiView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/customers', CustomerApiView.as_view()),
    path('api/v1/employees', EmployeeApiView.as_view()),

    path('api/v1/tasklist', TasklistApiView.as_view()),
    path('api/v1/tasklist/<int:pk>/take', TakeTaskApiView.as_view()),
    path('api/v1/tasklist/<int:pk>/finish', FinishTaskApiView.as_view()),

    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
