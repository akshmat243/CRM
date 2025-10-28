from django.db import models

class LoanRates(models.Model):
    code = models.CharField(max_length=255)
    bank_name = models.TextField()
    loan_type_id = models.IntegerField()
    rate = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'loan_rates'


class LoanTypes(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    # status = models.SmallIntegerField(db_comment='1=Active, 2=Deactive')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'loan_types'


class Loans(models.Model):
    user_id = models.IntegerField()
    loan_type_id = models.IntegerField(blank=True, null=True)
    requirement = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    mobile = models.BigIntegerField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    otp = models.IntegerField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    # status = models.IntegerField(db_comment='1 = Pending , 2 = Approve, 3 = Disapprove')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'loans'