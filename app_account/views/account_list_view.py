# =================================
# アカウント一覧クラス
# =================================
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from django.http import HttpResponseServerError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from app_account.models.account_model import AccountModel
from common.util_message import UtilMessage
from common.util_validation import UtilValidation
from common.util_authority import UtilAuthority
import logging

# ロガーを取得
logger = logging.getLogger(__name__)

class AccountListView(LoginRequiredMixin, TemplateView):
    # クラスラベル
    CLASS_LABEL = "アカウント一覧クラス"

    # テンプレートファイル
    template_name='app_account/member_list.html'

    def __init__(self):
        """
        コンストラクタ
        """
        # 共通パラメータ
        self.param = {
            "account_dataset": [], 
            "search_val_dict": {
                "name_or_id_or_email": "",
            }
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

            # 検索条件初期値
            search_val_dict = {
                "name_or_id_or_email":"",
            }

            account_dataset = []

            # アカウント一覧データセットを取得
            account_dataset = AccountModel.objects.values(
                'id', 
                'account_id',
                'account_name',
                'is_setup_completed',
                'member_number',
            ).filter(
                organization=request.user.organization,
            ).order_by('-is_active', 'account_id')

            # セッションに検索データがある場合
            if 'list_search_val_dict' in request.session:
                # セッションからデータを取得
                session_search_val_dict = self.request.session["list_search_val_dict"]

                # 検索条件を代入
                for key_name in search_val_dict:
                    if key_name in session_search_val_dict:
                        search_val_dict[key_name] = session_search_val_dict[key_name]
                
            # 検索
            if search_val_dict["name_or_id_or_email"]:
                account_dataset = account_dataset.filter(
                    Q(account_name__icontains=search_val_dict["name_or_id_or_email"]) |
                    Q(account_id__icontains=search_val_dict["name_or_id_or_email"]) 
                )

            # データ代入
            self.param["account_dataset"] = account_dataset
            self.param["search_val_dict"] = search_val_dict
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
            # データ取得
            # -------------------
            button_action = request.POST.get('button_action', '')
            account_id = request.POST.get('account_id', '')
            name_or_id_or_email = request.POST.get('name_or_id_or_email', '').strip()
            
            # ================
            # 削除処理の場合
            # ================
            if button_action == "account_delete":
                if not account_id or not UtilValidation.is_uuid(account_id):
                    messages.error(request, UtilMessage.Validation.E_INVALID_ID.format("メンバーアカウント"))
                    return redirect('app_account:member_list')
                
                try:
                    # 削除処理
                    account_obj = get_object_or_404(AccountModel, id=account_id)
                    delete_account_id = account_obj.account_id

                    # アカウントの組織が現在のユーザーの組織と異なる場合
                    if account_obj.organization != request.user.organization:
                        messages.error(request, UtilMessage.Validation.E_INVALID_ID.format("メンバーアカウント"))
                        return redirect('app_account:member_list')
                    # マネージャーアカウントの場合
                    if UtilAuthority.is_manager(account_obj.auth_code):
                        messages.error(request, UtilMessage.Browser.I_PLZ_ACTION.format("マネージャーアカウントの削除はできません。退会する場合は、組織管理ページから退会"))
                        return redirect('app_account:member_list')
                    
                    # アカウントを削除
                    account_obj.delete()
                    # メッセージ
                    messages.success(request, UtilMessage.Database.S_DELETE.format(f"アカウント（{delete_account_id}）"))
                    # リダイレクト
                    return redirect('app_account:member_list')
                except Exception as e:
                    # エラーメッセージ
                    messages.error(request, UtilMessage.Database.E_DELETE.format(f"アカウント（{delete_account_id}）"))

                
            # ================
            # 検索処理場合
            # ================
            elif  button_action == "account_search":
                # バリデーション
                is_validate_correct = True

                # 検索文字列のバリデーション
                if name_or_id_or_email:
                    if not UtilValidation.is_length_valid(name_or_id_or_email, 1, 32):
                        is_validate_correct = False
                        messages.error(request, UtilMessage.Validation.E_PLZ_INP_LENGTH.format("検索文字列", 1, 32))
                    elif UtilValidation.has_special_characters(name_or_id_or_email):
                        is_validate_correct = False
                        messages.error(request, UtilMessage.Validation.E_INVALID_CHAR.format("検索文字列"))

                # バリデーションエラーのない場合
                if is_validate_correct:
                    # -------------------
                    # データ保存
                    # -------------------
                    # セッションに代入
                    self.request.session["list_search_val_dict"] = {
                        "name_or_id_or_email": name_or_id_or_email,
                    }

                return redirect('app_account:member_list')

            # ==============================
            # ボタンアクションに該当がない場合
            # ==============================
            messages.error(request, UtilMessage.Browser.E_INVALID_REQUEST)
            return redirect('app_account:member_list')
        
        # ================
        # 例外処理:END
        # ================
        except Exception as e:
            # ログ出力
            logger.error(UtilMessage.Log.E_EXCEPT_POST.format(self.CLASS_LABEL, str(e)))
            # エラーレスポンスを返す
            return HttpResponseServerError(render(request, '500.html'))