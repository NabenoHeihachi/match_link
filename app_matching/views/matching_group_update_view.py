# =================================
# マッチンググループ更新クラス
# =================================
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.http import HttpResponseServerError, HttpResponseNotFound
from django.contrib.auth.mixins import LoginRequiredMixin
from common.util_authority import UtilAuthority
from common.util_message import UtilMessage
from django.db import transaction
from app_matching.forms.matching_group_forms import MatchingGroupInputForm, MatchingGroupCandidatesForm
from app_matching.models.matching_group_model import MatchingGroupModel
import logging

# ロガーの設定
logger = logging.getLogger(__name__)

class MatchingGroupUpdateView(LoginRequiredMixin, TemplateView):
    # クラスラベル
    CLASS_LABEL = "マッチンググループ更新クラス"

    # テンプレートファイル
    template_name = 'app_matching/matching_group_form.html'

    def __init__(self):
        self.param = {
            "matching_group_input_form": None,
            "matching_group_candidates_form": None,
            "is_detail": True
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
            # マッチンググループの取得
            # --------------------
            matching_group_id = kwargs.get('group_id', None)
            if not matching_group_id:
                messages.error(request, UtilMessage.Validation.E_INVALID_ID.format("マッチンググループ"))
                return redirect('app_matching:list')
            
            try:
                matching_group_instance = MatchingGroupModel.objects.get(
                    group_id=matching_group_id, 
                    organization=request.user.organization,
                    )
            except MatchingGroupModel.DoesNotExist:
                return HttpResponseNotFound(render(request, '404.html'))
            
            # パラメータにフォームを設定
            self.param["matching_group_input_form"] = MatchingGroupInputForm(
                instance=matching_group_instance,
                organization=request.user.organization
            )
            self.param["matching_group_candidates_form"] = MatchingGroupCandidatesForm(
                instance=matching_group_instance,
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
            
            # --------------------
            # マッチンググループの取得
            # --------------------
            matching_group_id = kwargs.get('group_id', None)
            if not matching_group_id:
                messages.error(request, UtilMessage.Validation.E_INVALID_ID.format("マッチンググループ"))
                return redirect('app_matching:list')
            
            try:
                matching_group_instance = MatchingGroupModel.objects.get(
                    group_id=matching_group_id, 
                    organization=request.user.organization,
                    )
            except MatchingGroupModel.DoesNotExist:
                return HttpResponseNotFound(render(request, '404.html'))
            
            if matching_group_instance.owner_account != request.user:
                messages.error(request, UtilMessage.Browser.E_NOT_AUTHORIZED)
                return redirect('app_matching:list')
            
            if matching_group_instance.is_matching_completed:
                messages.error(request, "マッチングが完了しているため、更新できません。")
                return redirect('app_matching:detail', group_id=matching_group_id)

            # --------------------
            # フォームを取得
            # --------------------
            matching_group_input_form = MatchingGroupInputForm(
                request.POST, 
                instance=matching_group_instance,
                organization=request.user.organization
            )
            matching_group_candidates_form = MatchingGroupCandidatesForm(
                request.POST, 
                instance=matching_group_instance,
                organization=request.user.organization
            )

            # フォームの検証
            if matching_group_input_form.is_valid() and matching_group_candidates_form.is_valid():
                # DB登録
                try:
                    # トランザクション開始
                    with transaction.atomic():
                        matching_group_form_instance = matching_group_input_form.save(commit=False)
                        matching_group_form_instance.organization = request.user.organization
                        matching_group_form_instance.owner_account = request.user
                        matching_group_form_instance.save()
                        matching_group_form_instance.matching_candidates.set(
                            matching_group_candidates_form.cleaned_data['matching_candidates']
                        )

                        # メッセージ表示
                        messages.success(request, UtilMessage.Database.S_UPDATE.format("マッチンググループ"))
                        return redirect('app_matching:detail', group_id=matching_group_id)
                        
                # DB保存エラー
                except Exception as e:
                    logger.error(UtilMessage.Database.E_UPDATE.format("マッチンググループ") + str(e))
                    messages.error(request, UtilMessage.Database.E_UPDATE.format("マッチンググループ"))

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