from django.contrib.auth.models import User
from django.test import TestCase
from .models import InvestmentAccount, UserPermission, Transaction

class InvestmentAccountTests(TestCase):
    def setUp(self):
        # Create an admin user with is_staff=True
        self.admin = User.objects.create_user(username='admin', password='adminpass', is_staff=True)
        
        # Create a regular user
        self.user = User.objects.create_user(username='user', password='userpass')
        
        # Create an investment account
        self.account = InvestmentAccount.objects.create(name='Test Account', balance=1000.00)
        
        # Assign permissions to the user
        self.permission = UserPermission.objects.create(
            user=self.user,
            investment_account=self.account,
            permission='view'
        )
        
        # Create a transaction
        self.transaction = Transaction.objects.create(
            investment_account=self.account,
            user=self.user,
            amount=100.00
        )

    def test_admin_user(self):
        # Check if the admin user has the is_staff flag set to True
        self.assertTrue(self.admin.is_staff)

    def test_regular_user(self):
        # Check if the regular user does not have is_staff flag set to True
        self.assertFalse(self.user.is_staff)

    def test_create_investment_account(self):
        # Verify the investment account was created
        account = InvestmentAccount.objects.get(name='Test Account')
        self.assertEqual(account.balance, 1000.00)

    def test_user_permission(self):
        # Verify the user permission was created correctly
        permission = UserPermission.objects.get(user=self.user, investment_account=self.account)
        self.assertEqual(permission.permission, 'view')

    def test_create_transaction(self):
        # Verify the transaction was created correctly
        transaction = Transaction.objects.get(user=self.user, investment_account=self.account)
        self.assertEqual(transaction.amount, 100.00)

    def test_get_admin_user_transactions(self):
        # Assuming you have a method or view to get transactions for admin
        # Here you should use the actual method or view to test
        transactions = Transaction.objects.filter(user=self.admin)
        self.assertEqual(transactions.count(), 0)  # Admin should have no transactions

    def test_get_user_transactions(self):
        # Verify transactions for a specific user
        transactions = Transaction.objects.filter(user=self.user)
        self.assertEqual(transactions.count(), 1)
        self.assertEqual(transactions[0].amount, 100.00)
