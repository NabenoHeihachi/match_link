# =================================
# アカウント更新クラス
# =================================
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import TemplateView
from django.http import HttpResponseServerError, HttpResponseNotFound
from app_account.forms.account_forms import MemberCreateForm
from app_account.models.account_model import AccountModel
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.http import Http404
from common.util_message import UtilMessage
from common.util_validation import UtilValidation
from common.util_authority import UtilAuthority
import logging

# ロガーの設定
logger = logging.getLogger(__name__)

class AccountUpdateView(LoginRequiredMixin, TemplateView):
    # クラスラベル
    CLASS_LABEL = "アカウント更新クラス"

    # テンプレートファイル
    template_name = 'app_account/member_form.html'

    def __init__(self):
        self.param = {
            "member_account_form": MemberCreateForm(),
            "is_detail": True,
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

            # -------------------
            # アカウント情報取得
            # -------------------
            # URLにIDがある場合
            if "account_id" in kwargs:
                # IDを取得
                account_id = kwargs["account_id"]
                # アカウントIDがない、またはUUID形式でない場合
                if not account_id or not UtilValidation.is_uuid(account_id):
                    messages.error(request, UtilMessage.Validation.E_INVALID_ID.format("アカウント"))
                    return redirect('app_account:member_list')
                
                # アカウント情報を取得
                account_data = None
                try:
                    account_data = get_object_or_404(AccountModel, id=account_id)
                except Http404:
                    return HttpResponseNotFound(render(request, '404.html'))
                
                # 同じ組織のアカウントでない場合
                if account_data.organization != request.user.organization:
                    return HttpResponseNotFound(render(request, '404.html'))
                
                self.param['member_account_form'] = MemberCreateForm(instance=account_data)

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
            # アカウント情報取得
            # -------------------
            account_data = None
            # URLにIDがある場合
            if "account_id" in kwargs:
                # IDを取得
                account_id = kwargs["account_id"]
                # アカウントIDがない、またはUUID形式でない場合
                if not account_id or not UtilValidation.is_uuid(account_id):
                    messages.error(request, UtilMessage.Validation.E_INVALID_ID.format("アカウント"))
                    return redirect('app_account:member_list')

                try:
                    account_data = get_object_or_404(AccountModel, id=account_id)
                except Http404:
                    return HttpResponseNotFound(render(request, '404.html'))

                # 同じ組織のアカウントでない場合
                if account_data.organization != request.user.organization:
                    return HttpResponseNotFound(render(request, '404.html'))
            
            if not account_data:
                messages.error(request, UtilMessage.Validation.E_INVALID_ID.format("アカウント"))
                return redirect('app_account:member_list')
                
            # -------------------
            # データバリデーション
            # -------------------
            member_form = MemberCreateForm(request.POST, instance=account_data)

            if member_form.is_valid():
                # -------------------
                # DB登録
                # -------------------
                try:
                    member_data = member_form.save(commit=False)
                    # パスワードが入力されている場合はハッシュ化
                    password = member_form.cleaned_data.get('password')
                    if password:
                        member_data.password = make_password(password)

                    member_data.updated_by = request.user.account_id
                    member_data.save()

                    messages.success(request, UtilMessage.Browser.S_ACTION_SUCCESS.format("メンバーアカウント更新"))
                    # リダイレクト
                    return redirect('app_account:member_list')
            
                # ユーニーク制約違反の場合
                except IntegrityError:
                    # メッセージ表示
                    messages.error(request, UtilMessage.Database.E_ALREADY_REGISTERED.format("ユーザーID"))

                except Exception as e:
                    logger.error(UtilMessage.Database.E_UPDATE.format("アカウント情報") + ":" + str(e))
                    messages.error(request, UtilMessage.Database.E_UPDATE.format("アカウント情報"))

            self.param['member_account_form'] = member_form
            return self.render_to_response(self.param)
        
        # ================
        # 例外処理:END
        # ================
        except Exception as e:
            # ログ出力
            logger.error(UtilMessage.Log.E_EXCEPT_POST.format(self.CLASS_LABEL, str(e)))
            # エラーレスポンスを返す
            return HttpResponseServerError(render(request, '500.html'))