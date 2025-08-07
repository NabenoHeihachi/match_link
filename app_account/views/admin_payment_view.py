# =================================
# アドミン支払い管理クラス
# =================================
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.http import HttpResponseServerError
from django.contrib.auth.mixins import LoginRequiredMixin
from common.util_message import UtilMessage
from app_account.forms.paymenthistory_forms import PaymentHistoryCreateForm
from app_account.models.paymenthistory_model import PaymentHistoryModel
from app_account.models.organization_model import OrganizationModel
from app_account.models.subscription_model import SubscriptionModel
# ログ
import logging

# ロガーの設定
logger = logging.getLogger(__name__)

class AdminPaymentView(LoginRequiredMixin, TemplateView):
    # クラスラベル
    CLASS_LABEL = "アドミン支払い管理クラス"

    # テンプレートファイル
    template_name = 'app_account/admin_payment.html'

    def __init__(self):
        self.param = {
            "payment_history_form": PaymentHistoryCreateForm(),
            "organization_dataset": None,
            "subscription_dataset": None,
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
            if not request.user.is_staff:
                # メッセージ表示
                messages.error(request, UtilMessage.Browser.E_NOT_AUTHORIZED)
                return redirect('app_account:control')
            
            self.param['organization_dataset'] = OrganizationModel.objects.all().order_by('organization_id')
            self.param['subscription_dataset'] = SubscriptionModel.objects.all().order_by('subscription_id')

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
            if not request.user.is_staff:
                # メッセージ表示
                messages.error(request, UtilMessage.Browser.E_NOT_AUTHORIZED)
                return redirect('app_account:control')

            # -------------------
            # データバリデーション
            # -------------------
            # フォームデータを取得
            payment_history_form = PaymentHistoryCreateForm(request.POST)

            organization_id = request.POST.get('organization_id', "")
            subscription_id = request.POST.get('subscription_id', "")

            try:
                organization_obj = OrganizationModel.objects.get(organization_id=organization_id)
                subscription_obj = SubscriptionModel.objects.get(subscription_id=subscription_id)
            except OrganizationModel.DoesNotExist:
                messages.error(request, UtilMessage.Browser.E_INVALID_REQUEST)
                return redirect('app_account:admin_payment')
            except SubscriptionModel.DoesNotExist:
                messages.error(request, UtilMessage.Browser.E_INVALID_REQUEST)
                return redirect('app_account:admin_payment')
            except Exception:
                messages.error(request, UtilMessage.Browser.E_INVALID_REQUEST)
                return redirect('app_account:admin_payment')

            if payment_history_form.is_valid():
                # -------------------
                # DB登録
                # -------------------
                try:
                    # トランザクション開始
                    with transaction.atomic():
                        # 支払い履歴の保存
                        payment_history = payment_history_form.save(commit=False)
                        payment_history.organization_id = organization_obj.organization_id
                        payment_history.organization_name = organization_obj.organization_name
                        payment_history.organization_email = organization_obj.organization_email
                        payment_history.payment_amount = subscription_obj.subscription_price
                        payment_history.subscription = subscription_obj
                        payment_history.payment_method = PaymentHistoryModel.PaymentMethod.OTHER
                        payment_history.payment_status = PaymentHistoryModel.PaymentStatus.PAID
                        payment_history.created_by = request.user.account_id
                        payment_history.updated_by = request.user.account_id
                        payment_history.save()

                        organization_obj.updated_by = request.user.account_id
                        organization_obj.subscription = subscription_obj
                        organization_obj.save()

                    messages.success(request, UtilMessage.Browser.S_ACTION_SUCCESS.format("現金支払い履歴新規作成"))
                    return redirect('app_account:admin_payment')

                except Exception as e:
                    logger.error(UtilMessage.Database.E_CREATE.format("現金支払い履歴新規作成") + ":" + str(e))
                    messages.error(request, UtilMessage.Database.E_UPDATE.format("現金支払い履歴"))

            self.param["payment_history_form"] = payment_history_form
            self.param['organization_dataset'] = OrganizationModel.objects.all().order_by('organization_id')
            self.param['subscription_dataset'] = SubscriptionModel.objects.all().order_by('subscription_id')
            
            return self.render_to_response(self.param)
        
        # ================
        # 例外処理:END
        # ================
        except Exception as e:
            # ログ出力
            logger.error(UtilMessage.Log.E_EXCEPT_POST.format(self.CLASS_LABEL, str(e)))
            # エラーレスポンスを返す
            return HttpResponseServerError(render(request, '500.html'))