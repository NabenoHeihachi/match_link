# =================================
# マッチンググループ作成クラス
# =================================
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.http import HttpResponseServerError
from django.contrib.auth.mixins import LoginRequiredMixin
from app_matching.models.matching_group_model import MatchingGroupModel
from common.util_authority import UtilAuthority
from common.util_message import UtilMessage
from django.db import transaction
from app_matching.forms.matching_group_forms import MatchingGroupInputForm, MatchingGroupCandidatesForm
import logging

# ロガーの設定
logger = logging.getLogger(__name__)

class MatchingGroupCreateView(LoginRequiredMixin, TemplateView):
    # クラスラベル
    CLASS_LABEL = "マッチンググループ作成クラス"

    # テンプレートファイル
    template_name = 'app_matching/matching_group_form.html'

    def __init__(self):
        self.param = {
            "matching_group_input_form": None,
            "matching_group_candidates_form": None,
            "is_detail": False
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
            
            self.param["matching_group_input_form"] = MatchingGroupInputForm(
                organization=request.user.organization
            )
            self.param["matching_group_candidates_form"] = MatchingGroupCandidatesForm(
                organization=request.user.organization
            )
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
                return redirect('app_matching:list')
            
            # ---------------
            # サブスクリプションチェック
            # ---------------
            matching_group_limit = 2
            if request.user.organization.subscription.matching_group_limit:
                matching_group_limit = request.user.organization.subscription.matching_group_limit

            # グループ数のチェック
            current_group_count = MatchingGroupModel.objects.filter(
                organization=request.user.organization,
                is_matching_completed=False
            ).count()

            if current_group_count >= matching_group_limit:
                messages.error(request, UtilMessage.Browser.E_PLZ_ACTIO.format(f"グループ数の上限に達しています。（現在のグループ数: {current_group_count}/上限: {matching_group_limit}）作成を続行するには、既存のグループを削除するか、サブスクリプションをアップグレード"))
                return redirect('app_matching:create')

            # フォームを取得
            matching_group_input_form = MatchingGroupInputForm(request.POST, organization=request.user.organization)
            matching_group_candidates_form = MatchingGroupCandidatesForm(request.POST, organization=request.user.organization)


            # フォームの検証
            if matching_group_input_form.is_valid() and matching_group_candidates_form.is_valid():
                # DB登録
                try:
                    # トランザクション開始
                    with transaction.atomic():
                        matching_group_instance = matching_group_input_form.save(commit=False)
                        matching_group_instance.organization = request.user.organization
                        matching_group_instance.owner_account = request.user
                        matching_group_instance.save()
                        matching_group_instance.matching_candidates.set(
                            matching_group_candidates_form.cleaned_data['matching_candidates']
                        )

                        # メッセージ表示
                        messages.success(request, UtilMessage.Browser.S_ACTION_SUCCESS.format("マッチンググループの作成"))
                        return redirect('app_matching:list')
                        
                # DB保存エラー
                except Exception as e:
                    logger.error(UtilMessage.Database.E_SAVE.format("マッチンググループ") + str(e))
                    messages.error(request, UtilMessage.Database.E_SAVE.format("マッチンググループ"))

            else:
                # エラーメッセージの表示
                messages.error(request, UtilMessage.Validation.E_PLZ_CHECK)
            
            # フォームのエラーをパラメータに追加
            self.param["matching_group_input_form"] = matching_group_input_form
            self.param["matching_group_candidates_form"] = matching_group_candidates_form

            return self.render_to_response(self.param)
        
        # ================
        # 例外処理:END
        # ================
        except Exception as e:
            # ログ出力
            logger.error(UtilMessage.Log.E_EXCEPT_POST.format(self.CLASS_LABEL, str(e)))
            # エラーレスポンスを返す
            return HttpResponseServerError(render(request, '500.html'))