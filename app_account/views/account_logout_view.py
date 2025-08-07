# ===========================
# ログアウトクラス
# ===========================
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.http import HttpResponseServerError
from django.contrib import messages
from common.util_message import UtilMessage
# ログ
import logging

# ロガーを取得
logger = logging.getLogger(__name__)


class AccountLogoutView(LoginRequiredMixin, TemplateView):
    # クラスラベル
    CLASS_LABEL = "ログアウトクラス"

    def __init__(self):
        # 共通パラメータ
        self.param = {}

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

            # ログアウト
            logout(request)
            # メッセージを表示
            messages.success(request, UtilMessage.Browser.S_ACTION_SUCCESS.format("ログアウト"))
            # リダイレクト
            return redirect("app_account:login")
        
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

            # ログアウト
            logout(request)
            # メッセージを表示
            messages.success(request, UtilMessage.Browser.S_ACTION_SUCCESS.format("ログアウト"))
            # リダイレクト
            return redirect("app_account:login")
        
        # ================
        # 例外処理:END
        # ================
        except Exception as e:
            # ログ出力
            logger.error(UtilMessage.Log.E_EXCEPT_POST.format(self.CLASS_LABEL, str(e)))
            # エラーレスポンスを返す
            return HttpResponseServerError(render(request, '500.html'))

