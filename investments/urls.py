from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AdminLoginView, AssignUserView, InvestmentAccountViewSet, RegisterAdminView, RegisterUserView,  UserLoginView, UserPermissionViewSet, TransactionViewSet, UserTransactionsView, UserViewSet, user_transactions

router = DefaultRouter()
router.register(r'investment-accounts', InvestmentAccountViewSet)
router.register(r'user-permissions', UserPermissionViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'users', UserViewSet)

urlpatterns = router.urls

# Admin endpoint for user transactions with total balance and date range filter
urlpatterns += [
    path('admin/user-transactions/<int:user_id>/', user_transactions, name='user-transactions'),
    path('api/investment-accounts/<int:account_id>/assign-user/', AssignUserView.as_view(), name='assign-user'),
    path('api/users/<str:username>/transactions/', UserTransactionsView.as_view(), name='user-transactions'),
    path('api/login/', UserLoginView.as_view(), name='user-login'),
    path('api/admin/login/', AdminLoginView.as_view(), name='admin-login'),
    path('api/signup/', RegisterUserView.as_view(), name='user-signup'),
    path('api/admin/signup/', RegisterAdminView.as_view(), name='admin-signup'),


]