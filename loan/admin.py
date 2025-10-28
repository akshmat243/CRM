from django.contrib import admin
from .models import *

@admin.register(LoanRates)
class LoanRatesAdmin(admin.ModelAdmin):
    list_display = ('code', 'bank_name', 'loan_type_id', 'rate', 'updated_at')
    search_fields = ('code', 'bank_name', 'loan_type_id')


@admin.register(LoanTypes)
class LoanTypesAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)


@admin.register(Loans)
class LoansAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'loan_type_id', 'name', 'mobile', 'updated_at')
    search_fields = ('name', 'mobile', 'email',)
    list_filter = [ 'loan_type_id']