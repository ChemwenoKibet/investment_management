from django.contrib import admin
from .models import InvestmentAccount, UserPermission, Transaction


# Register your models here.
@admin.register(InvestmentAccount)
class InvestmentAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'balance')

@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'investment_account', 'permission')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('investment_account', 'user', 'amount', 'timestamp')