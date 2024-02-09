from decimal import Decimal
from django.db import models

class Account(models.Model):
    account_id = models.CharField(primary_key=True, max_length=128, unique=True)
    balance = models.DecimalField(max_digits=17, decimal_places=2, default=0)

    def deposit(self, amount):
        amount = Decimal(amount)
        if amount > 0:
            self.balance += amount

    def withdraw(self, amount):
        amount = Decimal(amount)
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
