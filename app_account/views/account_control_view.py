# =================================
# アカウント認証設定クラス
# =================================
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.http import HttpResponseServerError
from django.contrib.auth.mixins import LoginRequiredMixin
from common.util_message import UtilMessage
from common.util_validation import UtilValidation
from common.util_authority import UtilAuthority
from axes.models import AccessLog
# ログ
import logging

# ロガーの設定
logger = logging.getLogger(__name__)

class AccountControlView(LoginRequiredMixin, TemplateView):
    # クラスラベル
    CLASS_LABEL = "アカウント管理クラス"

    # テンプレートファイル
    template_name = 'app_account/account_control.html'

    def __init__(self):
        """
        コンストラクタ
        """
        self.param = {
            "account_auth_code_dict": UtilAuthority.get_dict(),
            "account_activity_dataset": []
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

            account_activity_dataset = AccessLog.objects.filter(
                    username=request.user.account_id
                ).values(
                    "attempt_time",
                    "username",
                    "path_info",
                    "user_agent"
                ).order_by('-attempt_time')[:10]
            
            # データ代入
            self.param["account_activity_dataset"] = account_activity_dataset

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
        
            # -------------------
            # データ取得
            # -------------------
            button_action = request.POST.get('button_action', '')
            bf_new_password = request.POST.get('bf_new_password', '')
            bf_new_password_confirm = request.POST.get('bf_new_password_confirm', '')

            # --------------------
            # データチェック
            # --------------------
            # ボタンアクションのチェック
            if button_action not in ["change_password"]:
                # メッセージ出力
                messages.error(request, UtilMessage.Browser.E_INVALID_REQUEST)
                # リダイレクト
                return redirect("app_account:control")
            
            # ------------------------
            # パスワード更新の場合
            # ------------------------
            if button_action == "change_password":
                # パスワードバリデーション
                if not UtilValidation.is_match(bf_new_password, "password"):
                    # メッセージ表示
                    messages.error(request, UtilMessage.Validation.E_INVALID_PASSWORD)
                    return redirect("app_account:control")
                # パスワードの一致チェック
                if bf_new_password != bf_new_password_confirm:
                    # メッセージ表示
                    messages.error(request, UtilMessage.Validation.E_INVALID_PASSWORD_CONFIRM)
                    return redirect("app_account:control")

                # パスワードの更新処理
                request.user.set_password(bf_new_password)
                request.user.save(update_fields=["password"])
                messages.success(request, UtilMessage.Database.S_SAVE.format("新しいパスワード"))
                return redirect("app_account:control")

            # リダイレクト
            return redirect("app_account:control")
        
        # ================
        # 例外処理:END
        # ================
        except Exception as e:
            # ログ出力
            logger.error(UtilMessage.Log.E_EXCEPT_POST.format(self.CLASS_LABEL, str(e)))
            # エラーレスポンスを返す
            return HttpResponseServerError(render(request, '500.html'))