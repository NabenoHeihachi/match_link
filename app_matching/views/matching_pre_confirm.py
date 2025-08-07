# =================================
# マッチング開始前確認ビュー
# =================================
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.http import HttpResponseServerError, HttpResponseNotFound
from django.contrib.auth.mixins import LoginRequiredMixin
from common.util_message import UtilMessage
from app_matching.models.matching_group_model import MatchingGroupModel
from app_matching.models.matching_result_model import MatchingResultModel
from app_matching.forms.matching_result_froms import MatchingResultSelectMethodForm
import logging

# ロガーの設定
logger = logging.getLogger(__name__)

class MatchingPreConfirmView(LoginRequiredMixin, TemplateView):
    # クラスラベル
    CLASS_LABEL = "マッチング開始前確認ビュー"

    # テンプレートファイル
    template_name = 'app_matching/matching_pre_confirm.html'

    def __init__(self):
        self.param = {
            "matching_group_data": None,
            "matching_method_form": None,
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
                    is_matching_completed=False
                    )
            except MatchingGroupModel.DoesNotExist:
                return HttpResponseNotFound(render(request, '404.html'))

            if matching_group_instance.target_user != request.user:
                messages.error(request, UtilMessage.Browser.E_NOT_AUTHORIZED)
                return redirect('app_matching:list')
            
            # パラメータにフォームを設定
            self.param["matching_group_data"] = matching_group_instance
            self.param["matching_method_form"] = MatchingResultSelectMethodForm()

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
                    is_matching_completed=False
                    )
            except MatchingGroupModel.DoesNotExist:
                return HttpResponseNotFound(render(request, '404.html'))

            if matching_group_instance.target_user != request.user:
                messages.error(request, UtilMessage.Browser.E_NOT_AUTHORIZED)
                return redirect('app_matching:list')
            
            # --------------------
            # マッチング方法の選択
            # --------------------
            matching_method_form = MatchingResultSelectMethodForm(request.POST)
            if matching_method_form.is_valid():
                matching_method = matching_method_form.cleaned_data['matching_method']

                if matching_method == MatchingResultModel.MatchingMethod.HYBRID:
                    messages.success(request, UtilMessage.Browser.I_PLZ_ACTION.format("マッチング開始"))
                    return redirect('app_matching:matching_method_hybrid', group_id=matching_group_id)

                if matching_method == MatchingResultModel.MatchingMethod.AUTO:
                    return redirect('app_matching:matching_method_auto', group_id=matching_group_id)
                
                if matching_method == MatchingResultModel.MatchingMethod.MANUAL:
                    messages.success(request, UtilMessage.Browser.I_PLZ_ACTION.format("マッチング開始"))
                    return redirect('app_matching:matching_method_manual', group_id=matching_group_id)

                # 表示
                return redirect('app_matching:pre_confirm', group_id=matching_group_id)


            messages.error(request, UtilMessage.Validation.E_PLZ_SELECT.format("マッチング方法"))
            return redirect('app_matching:pre_confirm', group_id=matching_group_id)

        # ================
        # 例外処理:END
        # ================
        except Exception as e:
            # ログ出力
            logger.error(UtilMessage.Log.E_EXCEPT_POST.format(self.CLASS_LABEL, str(e)))
            # エラーレスポンスを返す
            return HttpResponseServerError(render(request, '500.html'))