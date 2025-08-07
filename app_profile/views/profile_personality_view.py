# =================================
# パーソナリティ管理ビュー
# =================================
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.http import HttpResponseServerError
from django.contrib.auth.mixins import LoginRequiredMixin
from common.util_message import UtilMessage
from app_profile.forms.personality_forms import PersonalityTagForm, BigFiveSurveyForm
from app_profile.models.personality_model import PersonalityModel
import logging

# ロガーの設定
logger = logging.getLogger(__name__)

class ProfilePersonalityView(LoginRequiredMixin, TemplateView):
    # クラスラベル
    CLASS_LABEL = "パーソナリティ管理ビュー"

    # テンプレートファイル
    template_name = 'app_profile/profile_personality.html'

    def __init__(self):
        self.param = {
            "personality_obj": None,
            "personality_tag_form": PersonalityTagForm(),
            "big_five_survey_form": BigFiveSurveyForm(),
            "big_five_rate": {}
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
            # セットアップ確認
            # --------------------
            if not request.user.is_setup_completed:
                # メッセージ表示
                messages.error(request, UtilMessage.Browser.E_PLZ_ACTIO.format("プロファイル初期セットアップ"))
                return redirect('app_profile:setup')
            
            # パーソナリティデータセットの取得
            personality_obj = PersonalityModel.objects.get(account=request.user, organization=request.user.organization)

            # 表示
            self.param["personality_obj"] = personality_obj
            self.param["personality_tag_form"] = PersonalityTagForm(instance=personality_obj)
            self.param["big_five_survey_form"] = BigFiveSurveyForm()
            self.param["big_five_rate"] = self.get_big_five_rate(personality_obj)

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
            # セットアップ確認
            # --------------------
            if not request.user.is_setup_completed:
                # メッセージ表示
                messages.error(request, UtilMessage.Browser.E_PLZ_ACTIO.format("プロファイル初期セットアップ"))
                return redirect('app_profile:setup')
            
            # --------------------
            # フォームの処理
            # --------------------
            button_action = request.POST.get('action', "")

            if button_action not in ["update-tags", "re-diagnose"]:
                # 不正なアクションの場合はエラーメッセージを表示
                messages.error(request, UtilMessage.Browser.E_INVALID_REQUEST)
                return redirect('app_profile:personality')

            # パーソナリティデータセットの取得
            personality_obj = PersonalityModel.objects.get(account=request.user, organization=request.user.organization)

            # --------------------
            # タグの更新
            # --------------------
            if button_action == "update-tags":
                # タグフォームの処理
                personality_tag_form = PersonalityTagForm(request.POST, instance=personality_obj)

                if personality_tag_form.is_valid():
                    # フォームの保存
                    try:
                        personality_tag_form.save()
                        # メッセージ表示
                        messages.success(request, UtilMessage.Database.S_UPDATE.format("パーソナリティタグ"))
                        return redirect('app_profile:personality')
                    except Exception as e:
                        # ログ出力
                        logger.error(UtilMessage.Database.E_UPDATE.format("パーソナリティタグ"), str(e))
                        # エラーメッセージ表示
                        messages.error(request, UtilMessage.Database.E_UPDATE.format("パーソナリティタグ"))

                else:
                    # エラーメッセージ表示
                    messages.error(request, UtilMessage.Browser.E_ACTION_ERROR.format("パーソナリティタグの更新"))
        

            # --------------------
            # 再診断の処理
            # --------------------
            elif button_action == "re-diagnose":
                # ビッグファイブの診断フォームの処理
                big_five_survey_form = BigFiveSurveyForm(request.POST)

                if big_five_survey_form.is_valid():
                    # フォームの保存
                    try:
                        # ビッグファイブのスコアを更新
                        big_five_form_data = big_five_survey_form.cleaned_data
                        personality_obj.big_five_openness = (
                            int(big_five_form_data['op_q1']) + 
                            int(big_five_form_data['op_q2']) + 
                            int(big_five_form_data['op_q3'])
                        )
                        personality_obj.big_five_conscientiousness = (
                            int(big_five_form_data['co_q1']) + 
                            int(big_five_form_data['co_q2']) + 
                            int(big_five_form_data['co_q3'])
                        )
                        personality_obj.big_five_extraversion = (
                            int(big_five_form_data['ex_q1']) + 
                            int(big_five_form_data['ex_q2']) + 
                            int(big_five_form_data['ex_q3'])
                        )
                        personality_obj.big_five_agreeableness = (
                            int(big_five_form_data['ag_q1']) + 
                            int(big_five_form_data['ag_q2']) + 
                            int(big_five_form_data['ag_q3'])
                        )
                        personality_obj.big_five_neuroticism = (
                            int(big_five_form_data['ne_q1']) + 
                            int(big_five_form_data['ne_q2']) + 
                            int(big_five_form_data['ne_q3'])
                        )
                        personality_obj.save()
                        # メッセージ表示
                        messages.success(request, UtilMessage.Database.S_UPDATE.format("パーソナリティ再診断"))
                        return redirect('app_profile:personality')
                    except Exception as e:
                        # ログ出力
                        logger.error(UtilMessage.Database.E_UPDATE.format("パーソナリティ再診断"), str(e))
                        # エラーメッセージ表示
                        messages.error(request, UtilMessage.Database.E_UPDATE.format("パーソナリティ再診断"))

                else:
                    # エラーメッセージ表示
                    messages.error(request, UtilMessage.Browser.E_ACTION_ERROR.format("パーソナリティ再診断"))

            # 表示
            self.param["personality_obj"] = personality_obj
            self.param["personality_tag_form"] = PersonalityTagForm(instance=personality_obj)
            self.param["big_five_survey_form"] = BigFiveSurveyForm()
            self.param["big_five_rate"] = self.get_big_five_rate(personality_obj)

            return self.render_to_response(self.param)
        
        # ================
        # 例外処理:END
        # ================
        except Exception as e:
            # ログ出力
            logger.error(UtilMessage.Log.E_EXCEPT_POST.format(self.CLASS_LABEL, str(e)))
            # エラーレスポンスを返す
            return HttpResponseServerError(render(request, '500.html'))
    

    def get_big_five_rate(self, personality_obj):
        """
        ビッグファイブの評価の割合を取得
        :param personality_obj: パーソナリティオブジェクト
        :return: ビッグファイブの評価の割合
        """
        MAX_SCORE = 15

        big_five_rate = {}

        big_five_scores = {
            "openness": personality_obj.big_five_openness,
            "conscientiousness": personality_obj.big_five_conscientiousness,
            "extraversion": personality_obj.big_five_extraversion,
            "agreeableness": personality_obj.big_five_agreeableness,
            "neuroticism": personality_obj.big_five_neuroticism
        }


        for key, score in big_five_scores.items():
            if score > 0 and score <= MAX_SCORE:
                big_five_rate[key] = round((score / MAX_SCORE) * 100)
            else:
                big_five_rate[key] = 0

        return big_five_rate