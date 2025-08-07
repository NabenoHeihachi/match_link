# ===========================
# ログインクラス
# ===========================
from time import sleep
from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseServerError
from django.contrib import messages
from common.util_message import UtilMessage
from common.util_validation import UtilValidation
# ログ
import logging

# ロガーを取得
logger = logging.getLogger(__name__)

class AccountLoginView(TemplateView):
    # クラスラベル
    CLASS_LABEL = "ログインクラス"

    # テンプレート
    template_name = "app_account/account_login.html"

    def __init__(self):
        self.param = {
            "created_account_id": "",
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

            created_account_id = request.session.pop('created_account_id', None)

            if created_account_id:
                self.param["created_account_id"] = created_account_id
        

            # データを表示
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

            # 文字数
            MIN_LEN = 8
            MAX_LEN = 64

            # リダイレクトURL初期位置
            redirect_url = "app_account:login"

            # -------------------
            # フォーム名をデータを取得
            # -------------------
            # 入力データ取得
            account_id = request.POST.get("account_id", "")[:MAX_LEN+1]
            account_password = request.POST.get("account_password", "")[:MAX_LEN+1]
            account_terms_agreement = request.POST.get("account_terms_agreement", "")

            # -------------------------------
            # 入力バリデーション
            # -------------------------------
            def is_valid_input(value):
                return (
                    UtilValidation.is_not_empty(value) and
                    UtilValidation.is_length_valid(value, MIN_LEN, MAX_LEN) and
                    not UtilValidation.has_special_characters(value)
                )

            is_valid = (
                is_valid_input(account_id) and
                is_valid_input(account_password)
            )

            if not is_valid:
                messages.error(request, UtilMessage.Validation.E_AUTH_FAILED)

            if account_terms_agreement != "agree":
                messages.error(request, UtilMessage.Validation.E_TERMS_REQUIRED)
                is_valid = False
            
            if not is_valid:
                return redirect(redirect_url)

            # -------------------
            # ユーザー認証処理
            # -------------------
            # ユーザー認証
            login_user = authenticate(request=request, account_id=account_id, password=account_password)

            # <<<<< ログインユーザーがない場合 >>>>>
            if login_user is None:
                messages.error(request, UtilMessage.Validation.E_AUTH_FAILED)

            # <<<<< ログインユーザーがある場合 >>>>>
            else:
                # ログイン
                login(request, login_user)

                redirect_url = "app_matching:list"
                messages.success(request, UtilMessage.Browser.S_ACTION_SUCCESS.format("ログイン"))

            return redirect(redirect_url)
        # ================
        # 例外処理:END
        # ================
        except Exception as e:
            # ログ出力
            logger.error(UtilMessage.Log.E_EXCEPT_POST.format(self.CLASS_LABEL, str(e)))
            # エラーレスポンスを返す
            return HttpResponseServerError(render(request, '500.html'))
