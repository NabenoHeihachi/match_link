from django.urls import path
from app_account.views.account_login_view import AccountLoginView
from app_account.views.account_logout_view import AccountLogoutView
from app_account.views.account_signup_view import AccountSignupView
from app_account.views.account_control_view import AccountControlView
from app_account.views.account_create_view import AccountCreateView
from app_account.views.account_update_view import AccountUpdateView
from app_account.views.account_list_view import AccountListView
from app_account.views.account_organization_view import AccountOrganizationView
from app_account.views.account_organization_delete_view import AccountOrganizationDeleteView
from app_account.views.admin_payment_view import AdminPaymentView

app_name = 'app_account'

urlpatterns = [
    path('login/', AccountLoginView.as_view(), name='login'),
    path('logout/', AccountLogoutView.as_view(), name='logout'),
    path('signup/', AccountSignupView.as_view(), name='signup'),

    path('', AccountControlView.as_view(), name='control'),
    path('create/', AccountCreateView.as_view(), name='member_create'),
    path('<str:account_id>/detail/', AccountUpdateView.as_view(), name='member_detail'),
    path('list/', AccountListView.as_view(), name='member_list'),
    path('organization/', AccountOrganizationView.as_view(), name='organization'),
    path('organization/delete/', AccountOrganizationDeleteView.as_view(), name='organization_delete'),

    path('admin/payment/', AdminPaymentView.as_view(), name='admin_payment'),
]