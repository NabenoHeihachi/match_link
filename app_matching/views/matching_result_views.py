# =================================
# マッチング結果一覧ビュー
# =================================
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.http import HttpResponseServerError
from django.contrib.auth.mixins import LoginRequiredMixin
from common.util_message import UtilMessage
from app_matching.models.matching_result_model import MatchingResultModel
import logging

# ロガーの設定
logger = logging.getLogger(__name__)

class MatchingResultListView(LoginRequiredMixin, TemplateView):
    # クラスラベル
    CLASS_LABEL = "マッチング結果一覧"

    # テンプレートファイル
    template_name = 'app_matching/matching_result_list.html'

    def __init__(self):
        self.param = {
            "matching_result_dataset": None,
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

            self.param["matching_result_dataset"] = MatchingResultModel.objects.filter(
                organization=request.user.organization,
                matching_group__is_matching_completed=True
            ).order_by('-result_id')

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


class MatchingResultDetailView(LoginRequiredMixin, TemplateView):
    # クラスラベル
    CLASS_LABEL = "マッチング結果詳細"

    # テンプレートファイル
    template_name = 'app_matching/matching_result_detail.html'

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

            result_id = kwargs.get('result_id', None)
            if not result_id:
                messages.error(request, UtilMessage.Validation.E_INVALID_ID.format("マッチング結果"))
                return redirect('app_matching:result_list')

            try:
                matching_result_instance = MatchingResultModel.objects.get(
                    result_id=result_id,
                    organization=request.user.organization
                )
            except MatchingResultModel.DoesNotExist:
                messages.error(request, UtilMessage.Validation.E_INVALID_ID.format("マッチング結果"))
                return redirect('app_matching:result_list')

            self.param = {
                "matching_result_data": matching_result_instance,
            }

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