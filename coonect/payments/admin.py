from django.contrib import admin

from payments.models import Card, Customer, Transaction


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    Admin class for Customer Model.
    """
    list_display = ('user', 'customer_uid',)
    list_display_links = ('user', 'customer_uid')


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    """
    Admin class for Card Model.
    """
    list_display = ('id', 'customer', 'last_4', 'expiration_date', 'card_type',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    Admin class for Transaction Model.
    """
    list_display = ('id', 'user', 'transaction_uid', 'amount', 'status',)
    list_filter = ('status',)
