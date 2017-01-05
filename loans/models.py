from django.db import models


class Loan(models.Model):
    # in pence
    MIN_AMOUNT = 1000000
    MAX_AMOUNT = 10000000
    company = models.ForeignKey(
        'customers.Company', null=True
    )
    amount = models.IntegerField()
    reason = models.TextField(null=True, blank=True)
    end_date = models.DateField()
