"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.authentication.views import RegisterView, CustomTokenObtainPairView, health_check
from apps.contracts.views import ContractViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from apps.core.views import home

# Create router and register viewsets
router = DefaultRouter()
router.register(r'contracts', ContractViewSet, basename='contract')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('api/register/', RegisterView.as_view(), name='register'),  # Registration route
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
    path('api/health/', health_check, name='health_check'),
]
