# =================================
# アカウントフォームクラス
# =================================
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.http import HttpResponseServerError
from app_account.forms.account_forms import MemberCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from common.util_message import UtilMessage
from common.util_authority import UtilAuthority
from app_account.models.account_model import AccountModel
import logging

# ロガーの設定
logger = logging.getLogger(__name__)

class AccountCreateView(LoginRequiredMixin, TemplateView):
    # クラスラベル
    CLASS_LABEL = "アカウント作成クラス"

    # テンプレートファイル
    template_name = 'app_account/member_form.html'

    def __init__(self):
        self.param = {
            "member_account_form": MemberCreateForm(),
            "is_detail": False,
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
            # フォームデータを取得
            member_form = MemberCreateForm(request.POST)


            last_created_member_account = AccountModel.objects.filter(
                organization=request.user.organization
            ).order_by('-member_number').first()

            member_number = last_created_member_account.member_number + 1

            # ---------------
            # サブスクリプションのチェック
            # ---------------
            account_limit = 2
            if request.user.organization.subscription.account_limit:
                account_limit = request.user.organization.subscription.account_limit
            
            # アカウント数のチェック
            current_account_count = AccountModel.objects.filter(
                organization=request.user.organization
            ).count()

            if current_account_count >= account_limit:
                messages.error(request, UtilMessage.Browser.E_PLZ_ACTIO.format(f"アカウント数の上限に達しています。（現在のアカウント数: {current_account_count}/上限: {account_limit}）作成を続行するには、既存のアカウントを削除するか、サブスクリプションをアップグレード"))
                return redirect('app_account:member_create')

            if member_form.is_valid():
                # -------------------
                # DB登録
                # -------------------
                try:
                    with transaction.atomic():
                        member_account = member_form.save(commit=False)
                        member_account.account_id = f"{request.user.organization.organization_id}{member_form.cleaned_data['account_id']}"
                        member_account.auth_code = UtilAuthority.get_dict()["メンバーアカウント"]
                        member_account.member_number = member_number
                        member_account.created_by = request.user.account_id
                        member_account.updated_by = request.user.account_id
                        # パスワードをハッシュ化
                        member_account.password = make_password(member_form.cleaned_data['password'])
                        # 組織を設定
                        member_account.organization = request.user.organization
                        member_account.save()

                        messages.success(request, UtilMessage.Browser.S_ACTION_SUCCESS.format("メンバーアカウント新規作成"))
                        return redirect('app_account:member_list')
                # ユーニーク制約違反の場合
                except IntegrityError:
                    # メッセージ表示
                    messages.error(request, UtilMessage.Database.E_ALREADY_REGISTERED.format(f"ユーザーID（{member_account.account_id}）"))

                except Exception as e:
                    logger.error(UtilMessage.Database.E_UPDATE.format("アカウント情報") + ":" + str(e))
                    messages.error(request, UtilMessage.Database.E_UPDATE.format("アカウント情報"))
                    
            self.param["member_account_form"] = member_form
            return self.render_to_response(self.param)
        
        # ================
        # 例外処理:END
        # ================
        except Exception as e:
            # ログ出力
            logger.error(UtilMessage.Log.E_EXCEPT_POST.format(self.CLASS_LABEL, str(e)))
            # エラーレスポンスを返す
            return HttpResponseServerError(render(request, '500.html'))