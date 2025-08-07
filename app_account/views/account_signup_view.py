# =================================
# サインアップビュー
# =================================
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.http import HttpResponseServerError
from django.contrib.auth.hashers import make_password
from app_account.forms.organization_forms import OrganizationSignupForm
from app_account.forms.account_forms import AccountSignupForm
from app_account.models.subscription_model import SubscriptionModel
from common.util_message import UtilMessage
from common.util_authority import UtilAuthority
from django.db import transaction, IntegrityError
import logging

# ロガーの設定
logger = logging.getLogger(__name__)

class AccountSignupView(TemplateView):
    # クラスラベル
    CLASS_LABEL = "サインアップビュー"

    # テンプレートファイル
    template_name = 'app_account/account_signup.html'

    def __init__(self):
        self.param = {
            "organization_form": OrganizationSignupForm(),
            "account_form": AccountSignupForm(),
        }

    def get(self, request, *args, **kwargs):
        """
        GET処理
        """
        # ================
        # 例外処理:START
        # ================
        try:
            # ログ出力
            logger.info(UtilMessage.Log.I_VIEW_GET.format(self.CLASS_LABEL))

            # ログインユーザーがある場合
            if request.user.is_authenticated:
                return redirect("app_account:control")

            # -------------------
            # アカウント情報取得
            # -------------------
            # 表示
            return self.render_to_response(self.param)
        # ================
        # 例外処理:END
        # ================
        except Exception as e:
            # ログ出力
            logger.error(UtilMessage.Log.E_EXCEPT_GET.format(self.CLASS_LABEL, str(e)))
            # エラーレスポンスを返す
            return HttpResponseServerError(render(request, '500.html'))

    def post(self, request, *args, **kwargs):
        """
        POST処理
        """
        # ================
        # 例外処理:START
        # ================
        try:
            # ログ出力
            logger.info(UtilMessage.Log.I_VIEW_POST.format(self.CLASS_LABEL))

            # ログインユーザーがある場合
            if request.user.is_authenticated:
                return redirect("app_account:control")

            organization_form = OrganizationSignupForm(request.POST)
            account_form = AccountSignupForm(request.POST)

            terms_agreement = request.POST.get("terms_agreement", "")

            if organization_form.is_valid() and account_form.is_valid() and terms_agreement == "agree":
                try:
                    with transaction.atomic():
                        free_subscription = SubscriptionModel.objects.get(subscription_name="Free")
                        
                        organization = organization_form.save(commit=False)
                        organization.created_by = request.user.username
                        organization.updated_by = request.user.username
                        organization.subscription = free_subscription
                        organization.save()

                        account = account_form.save(commit=False)
                        account.account_id = f"{organization.organization_id}{account_form.cleaned_data['account_id']}"
                        account.auth_code = UtilAuthority.get_dict()["管理アカウント"]
                        account.organization = organization
                        account.password = make_password(account_form.cleaned_data['password'])
                        account.save()

                    messages.success(request, UtilMessage.Browser.S_ACTION_SUCCESS.format("組織登録"))
                    # messages.warning(request, UtilMessage.Browser.I_PLZ_ACTION.format("IDは自動生成されました。確認"))
                    request.session['created_account_id'] = str(account.account_id)
                    return redirect('app_account:login')

                except IntegrityError as e:
                    messages.error(request, UtilMessage.Database.E_ALREADY_REGISTERED.format("入力されたアカウントIDまたはメールアドレス"))
                except Exception as e:
                    logger.error(UtilMessage.Database.E_SAVE.format("サインアップ情報") + str(e))
                    messages.error(request, UtilMessage.Database.E_SAVE.format("サインアップ情報"))

            if not organization_form.is_valid() or not account_form.is_valid():
                messages.error(request, UtilMessage.Validation.E_PLZ_CHECK)

            if terms_agreement != "agree":
                messages.error(request, UtilMessage.Validation.E_TERMS_REQUIRED)

            self.param['organization_form'] = organization_form
            self.param['account_form'] = account_form
            return self.render_to_response(self.param)
        
        # ================
        # 例外処理:END
        # ================
        except Exception as e:
            # ログ出力
            logger.error(UtilMessage.Log.E_EXCEPT_POST.format(self.CLASS_LABEL, str(e)))
            # エラーレスポンスを返す
            return HttpResponseServerError(render(request, '500.html'))