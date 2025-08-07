from django.contrib import admin
from app_account.models.subscription_model import SubscriptionModel
from app_account.models.organization_model import OrganizationModel
from app_account.models.account_model import AccountModel
from app_account.models.paymenthistory_model import PaymentHistoryModel


class AccountModelAdmin(admin.ModelAdmin):
    list_display = ('account_id', 'account_name', 'auth_code', 'organization__organization_name')
    search_fields = ('account_id', 'account_name')
    ordering = ('account_id',)
    list_filter = ('auth_code', 'organization__organization_name')

class OrganizationModelAdmin(admin.ModelAdmin):
    list_display = ('organization_id', 'organization_name',)
    search_fields = ('organization_name',)
    ordering = ('organization_name',)

class SubscriptionModelAdmin(admin.ModelAdmin):
    list_display = ('subscription_id', 'subscription_name', 'subscription_price')
    search_fields = ('subscription_name',)
    ordering = ('subscription_name',)

class PaymentHistoryModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization_name', 'subscription__subscription_name', 'payment_date',)
    ordering = ('-payment_date',)


admin.site.register(AccountModel, AccountModelAdmin)
admin.site.register(OrganizationModel, OrganizationModelAdmin)
admin.site.register(SubscriptionModel, SubscriptionModelAdmin)
admin.site.register(PaymentHistoryModel, PaymentHistoryModelAdmin)
admin.site.site_header = "MatchLink 管理システム"
admin.site.site_title = "MatchLink 管理システム"
admin.site.index_title = "MatchLink 管理システム"