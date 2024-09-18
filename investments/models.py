from django.db import models
from django.contrib.auth.models import User


# Create your models here.
PERMISSION_CHOICES = [
    ('view', 'View Only'),
    ('post', 'Post Transactions'),
    ('crud', 'Full Access (CRUD)'),
]

class InvestmentAccount(models.Model):
    """Model representing an investment account."""
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return self.name

class UserPermission(models.Model):
    """Model to assign permissions to users for specific investment accounts."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    investment_account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE)
    permission = models.CharField(max_length=10, choices=PERMISSION_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.investment_account.name} ({self.get_permission_display()})"

class Transaction(models.Model):
    """Model representing a transaction in an investment account."""
    investment_account = models.ForeignKey(InvestmentAccount, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction by {self.user.username} on {self.investment_account.name} for {self.amount}"
    

    