# =================================
# プロファイル初期セットアップビュー
# =================================
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.http import HttpResponseServerError
from app_profile.forms.profile_forms import ProfileImageForm, ProfileInputForm
from app_profile.forms.personality_forms import PersonalityTagForm, BigFiveSurveyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from common.util_message import UtilMessage
from django.db import transaction
import logging

# ロガーの設定
logger = logging.getLogger(__name__)

class ProfileSetupView(LoginRequiredMixin, TemplateView):
    # クラスラベル
    CLASS_LABEL = "プロファイル初期セットアップビュー"

    # テンプレートファイル
    template_name = 'app_profile/profile_setup.html'

    def __init__(self):
        self.param = {
            'profile_image_form': ProfileImageForm(),
            'profile_input_form': ProfileInputForm(),
            'personality_tag_form': PersonalityTagForm(),
            'big_five_survey_form': BigFiveSurveyForm(),
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
            if request.user.is_setup_completed:
                # メッセージ表示
                messages.error(request, UtilMessage.Browser.E_PLZ_ACTIO.format("プロファイル初期セットアップはすでに完了しています。確認"))
                return redirect('app_profile:profile')

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
            # セットアップ確認
            # --------------------
            if request.user.is_setup_completed:
                # メッセージ表示
                messages.error(request, UtilMessage.Browser.E_PLZ_ACTIO.format("プロファイル初期セットアップはすでに完了しています。確認"))
                return redirect('app_profile:profile')

            # フォームのバリデーション
            profile_image_form = ProfileImageForm(request.POST)
            profile_input_form = ProfileInputForm(request.POST)
            personality_tag_form = PersonalityTagForm(request.POST)
            big_five_survey_form = BigFiveSurveyForm(request.POST)

            if (
                profile_image_form.is_valid() and
                profile_input_form.is_valid() and
                personality_tag_form.is_valid() and
                big_five_survey_form.is_valid()
            ):
                # DB登録
                try:
                    # トランザクション開始
                    with transaction.atomic(): 
                        # プロファイル保存
                        profile_instance = profile_input_form.save(commit=False)
                        profile_instance.profile_image = profile_image_form.cleaned_data['profile_image']
                        profile_instance.account = request.user
                        profile_instance.organization = request.user.organization
                        profile_instance.save()

                        # パーソナリティ保存
                        personality_instance = personality_tag_form.save(commit=False)
                        big_five_form_data = big_five_survey_form.cleaned_data
                        personality_instance.big_five_openness = (
                            int(big_five_form_data['op_q1']) + 
                            int(big_five_form_data['op_q2']) + 
                            int(big_five_form_data['op_q3'])
                        )
                        personality_instance.big_five_conscientiousness = (
                            int(big_five_form_data['co_q1']) + 
                            int(big_five_form_data['co_q2']) + 
                            int(big_five_form_data['co_q3'])
                        )
                        personality_instance.big_five_extraversion = (
                            int(big_five_form_data['ex_q1']) + 
                            int(big_five_form_data['ex_q2']) + 
                            int(big_five_form_data['ex_q3'])
                        )
                        personality_instance.big_five_agreeableness = (
                            int(big_five_form_data['ag_q1']) + 
                            int(big_five_form_data['ag_q2']) + 
                            int(big_five_form_data['ag_q3'])
                        )
                        personality_instance.big_five_neuroticism = (
                            int(big_five_form_data['ne_q1']) + 
                            int(big_five_form_data['ne_q2']) + 
                            int(big_five_form_data['ne_q3'])
                        )
                        personality_instance.account = request.user
                        personality_instance.organization = request.user.organization
                        personality_instance.save()
                        personality_tag_form.save_m2m()

                        # ユーザーのセットアップ完了フラグを更新
                        request.user.is_setup_completed = True
                        request.user.save(update_fields=["is_setup_completed"])

                        # メッセージ表示
                        messages.success(request, UtilMessage.Browser.S_ACTION_SUCCESS.format("プロファイル初期セットアップ"))
                        return redirect('app_profile:profile')
                
                # DB保存エラー
                except Exception as e:
                    logger.error(UtilMessage.Database.E_SAVE.format("プロファイル初期セットアップ") + str(e))
                    messages.error(request, UtilMessage.Database.E_SAVE.format("プロファイル初期セットアップ"))
            
            else:
                # エラーメッセージの表示
                messages.error(request, UtilMessage.Validation.E_PLZ_CHECK)

            # フォームのエラーをパラメータにセット
            self.param['profile_image_form'] = profile_image_form
            self.param['profile_input_form'] = profile_input_form
            self.param['personality_tag_form'] = personality_tag_form
            self.param['big_five_survey_form'] = big_five_survey_form

            # 表示
            return self.render_to_response(self.param)
        
        # ================
        # 例外処理:END
        # ================
        except Exception as e:
            # ログ出力
            logger.error(UtilMessage.Log.E_EXCEPT_POST.format(self.CLASS_LABEL, str(e)))
            # エラーレスポンスを返す
            return HttpResponseServerError(render(request, '500.html'))