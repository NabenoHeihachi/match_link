# =================================
# プロファイル管理ビュー
# =================================
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.http import HttpResponseServerError
from django.contrib.auth.mixins import LoginRequiredMixin
from common.util_message import UtilMessage
from app_profile.models.profile_model import ProfileModel
from app_profile.forms.profile_forms import ProfileImageForm, ProfileInputForm

import logging

# ロガーの設定
logger = logging.getLogger(__name__)

class ProfileProfileView(LoginRequiredMixin, TemplateView):
    # クラスラベル
    CLASS_LABEL = "プロファイル管理ビュー"

    # テンプレートファイル
    template_name = 'app_profile/profile_profile.html'

    def __init__(self):
        self.param = {
            "profile_obj": None,
            "profile_image_form": ProfileImageForm(),
            "profile_input_form": ProfileInputForm(),
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
            

            # プロファイルデータセットの取得
            profile_obj = ProfileModel.objects.get(account=request.user, organization=request.user.organization)

            # 表示
            self.param["profile_obj"] = profile_obj
            self.param["profile_image_form"] = ProfileImageForm(instance=profile_obj)
            self.param["profile_input_form"] = ProfileInputForm(instance=profile_obj)
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
            
            # プロファイルデータセットの取得
            profile_obj = ProfileModel.objects.get(account=request.user, organization=request.user.organization)

            # -------------------
            # データバリデーション
            # -------------------
            profile_image_form = ProfileImageForm(request.POST, instance=profile_obj)
            profile_input_form = ProfileInputForm(request.POST, instance=profile_obj)

            if profile_image_form.is_valid() and profile_input_form.is_valid():
                # データの保存
                try:
                    profile_image_form.save()
                    profile_input_form.save()
                    messages.success(request, UtilMessage.Database.S_UPDATE.format("プロフィール情報"))
                    return redirect('app_profile:profile')
                
                except Exception as e:
                    logger.error(UtilMessage.Database.E_UPDATE.format("プロフィール情報"), str(e))
                    messages.error(request, UtilMessage.Database.E_UPDATE.format("プロフィール情報"))
            else:
                # エラーメッセージの表示
                messages.error(request, UtilMessage.Validation.E_PLZ_CHECK)
            

                
            self.param["profile_obj"] = profile_obj
            self.param["profile_image_form"] = profile_image_form
            self.param["profile_input_form"] = profile_input_form
            return self.render_to_response(self.param)

        # ================
        # 例外処理:END
        # ================
        except Exception as e:
            # ログ出力
            logger.error(UtilMessage.Log.E_EXCEPT_POST.format(self.CLASS_LABEL, str(e)))
            # エラーレスポンスを返す
            return HttpResponseServerError(render(request, '500.html'))