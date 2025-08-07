# =================================
# 自動型マッチングビュー
# =================================
from time import sleep
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.http import HttpResponseServerError, HttpResponseNotFound
from django.contrib.auth.mixins import LoginRequiredMixin
from common.util_message import UtilMessage
from common.util_llm import UtilLLM
from common.util_matching import UtilMatching
from app_matching.models.matching_group_model import MatchingGroupModel
from app_matching.models.matching_result_model import MatchingResultModel
from app_account.models.account_model import AccountModel
from app_profile.models.personality_model import PersonalityModel
from app_profile.models.profile_model import ProfileModel
from django.db import transaction
import logging

# ロガーの設定
logger = logging.getLogger(__name__)

class MatchingMethodAutoView(LoginRequiredMixin, TemplateView):
    # クラスラベル
    CLASS_LABEL = "自動型マッチングビュー"

    # テンプレートファイル
    template_name = 'app_matching/matching_method_auto.html'

    def __init__(self):
        self.param = {
            "candidate_data": None,
            "ai_reason_summary": "",
            "result_id": None,
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

            result_id = None

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
            # 候補者を取得
            # --------------------
            candidate_dataset = []
            account_personality = PersonalityModel.objects.get(account=request.user)
            for candidate_account in matching_group_instance.matching_candidates.all():
                # 候補者のパーソナリティを取得
                candidate_personality = PersonalityModel.objects.get(account=candidate_account)
                # マッチングスコアを計算
                match_score = UtilMatching().calculate_matching_score(account_personality, candidate_personality)
                candidate_dataset.append({
                    'account': candidate_account,
                    'profile': ProfileModel.objects.get(account=candidate_account),
                    'match_score': match_score
                })
            
            # スコアの高い候補者を選択
            candidate_data = sorted(candidate_dataset, key=lambda x: x['match_score'], reverse=True)[0]

            try:
                candidate_account = candidate_data['account']
                match_score = candidate_data['match_score']

                try:
                    ai_reason_summary = UtilLLM.generate_match_reason(
                            target_account=request.user,
                            candidate_account=candidate_account
                        )
                except Exception as e:
                    ai_reason_summary = "サマリー生成に失敗しました。"

                with transaction.atomic():
                    result_object = MatchingResultModel.objects.create(
                        matching_group=matching_group_instance,
                        organization=request.user.organization,
                        voter=request.user,
                        chosen_person=candidate_account,
                        match_score=match_score,
                        reason_summary=ai_reason_summary,
                        matching_method=MatchingResultModel.MatchingMethod.AUTO
                    )

                    matching_group_instance.is_matching_completed = True
                    matching_group_instance.save()

                messages.success(request, f"自動マッチングが完了しました。")
                # マッチンググループデータをパラメータに設定
                self.param['candidate_data'] = candidate_data
                self.param['ai_reason_summary'] = ai_reason_summary
                self.param['result_id'] = result_object.result_id
                # 表示
                return self.render_to_response(self.param)
            
            except Exception as e:
                logger.error(UtilMessage.Database.E_UPDATE.format("ハイブリット型マッチング結果") + str(e))
                messages.error(request, UtilMessage.Database.E_UPDATE.format("ハイブリット型マッチング結果"))
            
            return redirect('app_matching:list')
        # ================
        # 例外処理:END
        # ================
        except Exception as e:
            # ログ出力
            logger.error(UtilMessage.Log.E_EXCEPT_GET.format(self.CLASS_LABEL, str(e)))
            # エラーレスポンスを返す
            return HttpResponseServerError(render(request, '500.html'))
