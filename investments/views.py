from django.shortcuts import render,get_object_or_404
from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .models import InvestmentAccount, UserPermission, Transaction
from .permissions import IsAccountOwnerOrAdmin, IsAccountViewer, IsAccountCRUDUser, IsTransactionPoster
from .serializers import InvestmentAccountSerializer, UserPermissionSerializer, TransactionSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Sum
from rest_framework import permissions
from django.utils.dateparse import parse_datetime
from .models import Transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsAdminUserJWT 
from rest_framework import viewsets
from .models import InvestmentAccount
from .serializers import InvestmentAccountSerializer
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserSerializer

from .serializers import (
    InvestmentAccountSerializer,
    UserPermissionSerializer,
    TransactionSerializer,
    UserSerializer
)
@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def user_transactions(request, user_id):
    """
    Admin endpoint to return all transactions of a specific user with a total balance,
    and a date range filter for transactions.
    """
    # Retrieve date range from query parameters
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    # Get user's transactions, optionally filtering by date range
    transactions = Transaction.objects.filter(user_id=user_id)
    
    if start_date:
        start_date = parse_datetime(start_date)
        transactions = transactions.filter(timestamp__gte=start_date)
    
    if end_date:
        end_date = parse_datetime(end_date)
        transactions = transactions.filter(timestamp__lte=end_date)

    # Calculate total balance from all transactions
    total_balance = transactions.aggregate(Sum('amount'))['amount__sum'] or 0

    # Serialize transactions
    serializer = TransactionSerializer(transactions, many=True)

    return Response({
        'transactions': serializer.data,
        'total_balance': total_balance
    })
     

class RegisterUserView(APIView):
    """
    View to handle regular user registration.
    """
    def post(self, request):
        data = request.data
        data['is_staff'] = False  # regular users do not get admin privileges
        serializer = UserSerializer(data=data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User created successfully',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RegisterAdminView(APIView):
    """
    View to handle admin registration.
    Any user accessing this route can sign up as an admin.
    """
    def post(self, request):
        data = request.data
        data['is_staff'] = True  
        serializer = UserSerializer(data=data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Admin created successfully',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    """
    View for user login at /api/login/
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None and not user.is_staff:
            # Create JWT tokens indicating the user is not an admin
            refresh = RefreshToken.for_user(user)
            refresh['is_admin'] = False  
            
            return Response({
                'message': 'Logged in successfully',
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials or not a regular user'}, status=status.HTTP_401_UNAUTHORIZED)

class AdminLoginView(APIView):
    """
    View for admin login at /api/admin/login/
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:  # Check if the user is an admin
            # Create JWT tokens with a custom claim indicating the user is an admin
            refresh = RefreshToken.for_user(user)
            refresh['is_admin'] = True  # Add custom claim for admin
            
            return Response({
                'message': 'Admin logged in successfully',
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials or not an admin'}, status=status.HTTP_401_UNAUTHORIZED)




class UserPermissionViewSet(viewsets.ModelViewSet):
    """ViewSet for managing user permissions for investment accounts."""
    queryset = UserPermission.objects.all()
    serializer_class = UserPermissionSerializer
    permission_classes = [permissions.IsAuthenticated]

class TransactionViewSet(viewsets.ModelViewSet):
    """ViewSet for handling CRUD operations for Transactions."""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for handling CRUD operations for Users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAdminUser]
    def get_permissions(self):
        if self.action == 'create':
            # Allow only users with 'post' permission to create transactions
            self.permission_classes = [permissions.IsAuthenticated & IsTransactionPoster]
        else:
            # Deny all other actions (like viewing or editing) for 'post' permission users
            self.permission_classes = [permissions.IsAuthenticated & IsAccountCRUDUser]
        return super().get_permissions()
    
class AssignUserView(APIView):
    permission_classes = [IsAdminUser]  # Only admins can assign users

    def post(self, request, account_id):
        # Get investment account by id
        investment_account = get_object_or_404(InvestmentAccount, id=account_id)

        # Get user by username
        username = request.data.get('username')
        if not username:
            return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, username=username)

        # Get permission from the request
        permission = request.data.get('permission')
        if permission not in ['view', 'crud', 'post']:
            return Response({'error': 'Invalid permission type'}, status=status.HTTP_400_BAD_REQUEST)

        # Create or update user permission for the investment account
        user_permission, created = UserPermission.objects.update_or_create(
            user=user, investment_account=investment_account,
            defaults={'permission': permission}
        )

        # Serialize and return the user permission
        serializer = UserPermissionSerializer(user_permission)
        return Response({
            'message': f'{user.username} assigned {permission} permission to account {investment_account.id}.',
            'user_permission': serializer.data
        }, status=status.HTTP_200_OK)
    
class UserTransactionsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        transactions = Transaction.objects.filter(user=user)
        serializer = TransactionSerializer(transactions, many=True)
        
        total_balance = transactions.aggregate(total_balance=Sum('amount'))['total_balance'] or 0
        
        return Response({
            'transactions': serializer.data,
            'total_balance': total_balance
        })
    
class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admins to view transactions.
    """

    def has_permission(self, request, view):
        # Allow read permissions only if the user is an admin
        if request.method in ['GET']:
            return request.user and request.user.is_staff
        # Allow all authenticated users to post transactions
        return request.method in ['POST'] and request.user and request.user.is_authenticated    
    

class InvestmentAccountTransactionsView(APIView):
    permission_classes = [IsAuthenticated, IsAccountOwnerOrAdmin]

    def get(self, request, pk):
        investment_account = get_object_or_404(InvestmentAccount, pk=pk)
        
        # Check if the user has permission to view this account's transactions
        self.check_object_permissions(request, investment_account)
        
        transactions = Transaction.objects.filter(investment_account=investment_account)
        serializer = TransactionSerializer(transactions, many=True)
        return Response({'transactions': serializer.data})

    def post(self, request, pk):
        investment_account = get_object_or_404(InvestmentAccount, pk=pk)
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            # Make sure to handle the association here
            serializer.save(investment_account=investment_account, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class UserTransactionsView(APIView):
    def get(self, request, username, format=None):
        # Filter transactions by username
        transactions = Transaction.objects.filter(user__username=username)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InvestmentAccountViewSet(viewsets.ModelViewSet):
    queryset = InvestmentAccount.objects.all()
    serializer_class = InvestmentAccountSerializer