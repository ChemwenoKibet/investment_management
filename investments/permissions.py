from rest_framework import permissions
from .models import UserPermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import BasePermission


class IsAccountViewer(permissions.BasePermission):
    """
    Custom permission to allow view-only access to an investment account.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Check if user has 'view' permission for this account
            permission = UserPermission.objects.filter(
                user=request.user, 
                investment_account=obj, 
                permission='view'
            ).exists()
            return permission
        return False

class IsAccountCRUDUser(permissions.BasePermission):
    """
    Custom permission to allow full CRUD (Create, Read, Update, Delete) access.
    """
    def has_object_permission(self, request, view, obj):
        permission = UserPermission.objects.filter(
            user=request.user, 
            investment_account=obj, 
            permission='crud'
        ).exists()
        return permission

class IsTransactionPoster(permissions.BasePermission):
    """
    Custom permission to allow only posting of transactions without view access.
    """
    def has_permission(self, request, view):
        # Only allow POST method for users with 'post' permission
        if request.method == 'POST':
            return UserPermission.objects.filter(
                user=request.user, 
                investment_account=view.kwargs.get('investment_account_pk'), 
                permission='post'
            ).exists()
        return False

class IsAdminUserJWT(BasePermission):
    """
    Allows access only to admin users based on the JWT token.
    """
    
    def has_permission(self, request, view):
        # Get the JWT token and decode it
        jwt_auth = JWTAuthentication()
        auth_result = jwt_auth.authenticate(request)

        if auth_result is not None:
            user, token = auth_result
            # Check if 'is_admin' claim exists and is set to True
            return token.get('is_admin', False)
        
        # If authentication fails or 'is_admin' claim is not present, deny access
        return False
    

class IsAccountOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow the account owner or admin to view transactions.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is an admin or the owner of the investment account
        return request.user.is_staff or obj.user == request.user    