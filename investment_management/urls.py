"""
URL configuration for investment_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from investments.views import AdminLoginView, AssignUserView, InvestmentAccountTransactionsView,  RegisterAdminView, RegisterUserView,  UserLoginView, UserTransactionsView, user_transactions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('investments.urls')),
    path('admin/user-transactions/<int:user_id>/', user_transactions, name='user-transactions'),
    path('api/investment-accounts/<int:account_id>/assign-user/', AssignUserView.as_view(), name='assign-user'),
    path('api/users/<str:username>/transactions/', UserTransactionsView.as_view(), name='user-transactions'),
    path('api/investment-accounts/<int:pk>/transactions/', InvestmentAccountTransactionsView.as_view(), name='investment-account-transactions'),
    path('api/login/', UserLoginView.as_view(), name='user-login'),
    path('api/admin/login/', AdminLoginView.as_view(), name='admin-login'),
    path('api/signup/', RegisterUserView.as_view(), name='user-signup'),
    path('api/admin/signup/', RegisterAdminView.as_view(), name='admin-signup'),


]