from rest_framework import serializers
from django.contrib.auth.models import User
from .models import InvestmentAccount, UserPermission, Transaction
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class InvestmentAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentAccount
        fields = ['id', 'name', 'balance']

class UserPermissionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    investment_account = serializers.StringRelatedField()

    class Meta:
        model = UserPermission
        fields = ['id', 'user', 'investment_account', 'permission']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'investment_account', 'user', 'amount', 'timestamp']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email','password', 'first_name', 'last_name', 'is_staff']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data) 


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'