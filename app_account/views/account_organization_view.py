# =================================
# アカウント組織管理クラス
# =================================
from time import sleep
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.http import HttpResponseServerError
from app_account.models.paymenthistory_model import PaymentHistoryModel
from app_account.forms.organization_forms import OrganizationUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from common.util_message import UtilMessage
from common.util_authority import UtilAuthority
import logging

# ロガーの設定
logger = logging.getLogger(__name__)

class AccountOrganizationView(LoginRequiredMixin, TemplateView):
    # クラスラベル
    CLASS_LABEL = "アカウント組織管理クラス"

    # テンプレートファイル
    template_name = 'app_account/account_organization.html'

    def __init__(self):
        self.param = {
            "organization_form": OrganizationUpdateForm(),
            "payment_history_dataset": [],
            "start_date": None,
            "expiration_date": None,
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

            # --------------------
            # 権限チェック
            # --------------------
            if not UtilAuthority.is_manager(request.user.auth_code):
                # メッセージ表示
                messages.error(request, UtilMessage.Browser.E_NOT_AUTHORIZED)
                return redirect('app_account:control')

            self.param['organization_form'] = OrganizationUpdateForm(instance=request.user.organization)
            self.param['payment_history_dataset'] = PaymentHistoryModel.objects.filter(
                organization_id=request.user.organization.organization_id
            ).order_by('-payment_date')

            if self.param['payment_history_dataset']:
                self.param['start_date'] = self.param['payment_history_dataset'][0].start_date
                self.param['expiration_date'] = self.param['payment_history_dataset'][0].expiration_date

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

            # --------------------
            # 権限チェック
            # --------------------
            if not UtilAuthority.is_manager(request.user.auth_code):
                # メッセージ表示
                messages.error(request, UtilMessage.Browser.E_NOT_AUTHORIZED)
                return redirect('app_account:control')

            
            # -------------------
            # データバリデーション
            # -------------------
            organization_form = OrganizationUpdateForm(request.POST, instance=request.user.organization)

            if organization_form.is_valid():
                # -------------------
                # DB登録
                # -------------------
                try:
                    organization_data = organization_form.save(commit=False)
                    organization_data.updated_by = request.user.account_id
                    organization_data.save()

                    messages.success(request, UtilMessage.Browser.S_ACTION_SUCCESS.format("更新"))
                    # リダイレクト
                    return redirect('app_account:organization')
                
                except Exception as e:
                    logger.error(UtilMessage.Database.E_UPDATE.format("組織情報更新") + ":" + str(e))
                    messages.error(request, UtilMessage.Database.E_UPDATE.format("組織情報更新"))

            self.param['organization_form'] = organization_form
            self.param['payment_history_dataset'] = PaymentHistoryModel.objects.filter(
                organization_id=request.user.organization.organization_id
            ).order_by('-payment_date')

            if self.param['payment_history_dataset']:
                self.param['start_date'] = self.param['payment_history_dataset'][0].start_date
                self.param['expiration_date'] = self.param['payment_history_dataset'][0].expiration_date

            return self.render_to_response(self.param)
        
        # ================
        # 例外処理:END
        # ================
        except Exception as e:
            # ログ出力
            logger.error(UtilMessage.Log.E_EXCEPT_POST.format(self.CLASS_LABEL, str(e)))
            # エラーレスポンスを返す
            return HttpResponseServerError(render(request, '500.html'))
