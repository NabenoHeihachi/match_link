# =================================
# アカウント組織削除クラス
# =================================
from time import sleep
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.http import HttpResponseServerError
from django.contrib.auth.mixins import LoginRequiredMixin
from common.util_message import UtilMessage
from common.util_authority import UtilAuthority
from app_account.models.organization_model import OrganizationModel
from app_account.models.account_model import AccountModel
from app_matching.models.matching_group_model import MatchingGroupModel
from app_matching.models.matching_result_model import MatchingResultModel
from app_profile.models.personality_model import PersonalityModel
from app_profile.models.profile_model import ProfileModel
from django.db import transaction
import logging

# ロガーの設定
logger = logging.getLogger(__name__)

class AccountOrganizationDeleteView(LoginRequiredMixin, TemplateView):
    """
    アカウント組織削除クラス
    """
    # クラスラベル
    CLASS_LABEL = "アカウント組織削除クラス"

    def post(self, request, *args, **kwargs):
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

            # --------------------
            # トランザクション開始
            # --------------------
            try:
                with transaction.atomic():
                    # 組織情報の取得
                    organization_obj = request.user.organization

                    # マッチンググループとマッチング結果の削除
                    MatchingGroupModel.objects.filter(organization=organization_obj).delete()
                    MatchingResultModel.objects.filter(organization=organization_obj).delete()

                    # パーソナリティとプロフィールの削除
                    PersonalityModel.objects.filter(organization=organization_obj).delete()
                    ProfileModel.objects.filter(organization=organization_obj).delete()

                    # アカウントを削除
                    AccountModel.objects.filter(organization=organization_obj).delete()

                    # 組織情報を削除
                    OrganizationModel.objects.filter(organization_id=organization_obj.organization_id).delete()

                    # メッセージを表示
                    messages.success(request, UtilMessage.Browser.S_ACTION_SUCCESS.format("退会"))
                    messages.success(request, "組織情報と全てのアカウント情報が完全に削除されました。")
                    return redirect('app_document:index')
            except Exception as e:
                # ログ出力
                logger.error(UtilMessage.Database.E_DELETE.format(self.CLASS_LABEL, str(e)))
                messages.error(request, "組織情報の削除中にエラーが発生しました。")
                return HttpResponseServerError(render(request, '500.html'))
            
            # メッセージ
            messages.success(request, UtilMessage.Browser.E_ACTION_ERROR.format("組織削除"))
            # リダイレクト
            return redirect('app_account:organization')
    
        # ================
        # 例外処理:END
        # ================
        except Exception as e:
            # ログ出力
            logger.error(UtilMessage.Log.E_EXCEPT_POST.format(self.CLASS_LABEL, str(e)))
            # エラーレスポンスを返す
            return HttpResponseServerError(render(request, '500.html'))
