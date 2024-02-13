from decimal import Decimal
from django.db import models

class Account(models.Model):
    id = models.CharField(primary_key=True, max_length=128, unique=True)
    _balance = models.DecimalField(max_digits=17, decimal_places=2, default=0)

    def deposit(self, amount):
        amount = Decimal(amount)
        if amount > 0:
            self.balance += amount

    def withdraw(self, amount):
        amount = Decimal(amount)
        if amount > 0 and amount <= self.balance:
            self.balance -= amount

    @property
    def balance(self):
        if self._balance % 1 == 0:
            return int(self._balance)
        else:
            return self._balance

    @balance.setter
    def balance(self, value):
        self._balance = value
