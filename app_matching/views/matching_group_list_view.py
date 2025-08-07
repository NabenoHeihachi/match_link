# =================================
# マッチンググループ一覧クラス
# =================================
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.http import HttpResponseServerError
from django.contrib.auth.mixins import LoginRequiredMixin
from common.util_message import UtilMessage
from django.db.models import Q
from app_matching.models.matching_group_model import MatchingGroupModel
import logging

from common.util_validation import UtilValidation

# ロガーの設定
logger = logging.getLogger(__name__)

class MatchingGroupListView(LoginRequiredMixin, TemplateView):
    # クラスラベル
    CLASS_LABEL = "マッチンググループ一覧クラス"

    # テンプレートファイル
    template_name = 'app_matching/matching_group_list.html'

    def __init__(self):
        self.param = {
            "your_matching_group_dataset": None,
            "matching_group_dataset": None,
            "matched_group_dataset": None,
            "search_keyword": "",
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

            search_keyword = ""
            your_matching_group_dataset = None
            matching_group_dataset = None
            matched_group_dataset = None

            # マッチンググループ一覧を取得
            all_matching_group_dataset = MatchingGroupModel.objects.filter(
                organization=request.user.organization,
                ).order_by('-created_at')
            
            # マッチンググループ一覧を取得
            matching_group_dataset = all_matching_group_dataset.filter(
                is_matching_completed=False
                ).order_by('-created_at')
            
            # マッチンググループ一覧を取得
            matched_group_dataset = all_matching_group_dataset.filter(
                is_matching_completed=True,
                ).order_by('-created_at')

            # セッションに検索データがある場合
            if 'matching_group_search_keyword' in request.session:
                # セッションからデータを取得
                search_keyword = request.session["matching_group_search_keyword"]

            # 検索
            if search_keyword:
                matching_group_dataset = matching_group_dataset.filter(
                    Q(group_name__icontains=search_keyword) |
                    Q(group_description__icontains=search_keyword)
                )
            
            # ユーザが対象のマッチンググループを取得
            your_matching_group_dataset = matching_group_dataset.filter(
                target_user=request.user
            ).order_by('-created_at')

            # パラメータにデータセットを設定
            self.param["search_keyword"] = search_keyword
            self.param["your_matching_group_dataset"] = your_matching_group_dataset
            self.param["matching_group_dataset"] = matching_group_dataset
            self.param["matched_group_dataset"] = matched_group_dataset

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

            # -------------------
            # データ取得
            # -------------------
            button_action = request.POST.get('action', '').strip()
            group_id = request.POST.get('group_id', '').strip()
            search_keyword = request.POST.get('search_keyword', '').strip()

            # ================
            # 削除処理の場合
            # ================
            if button_action == "delete":
                # バリデーション
                is_validate_correct = True
                matching_group_obj = None

                if not group_id or not UtilValidation.is_convertible_to_number(group_id):
                    is_validate_correct = False
                    messages.error(request, UtilMessage.Validation.E_INVALID_ID.format("マッチンググループ"))
                
                if is_validate_correct:
                    try:
                        matching_group_obj = MatchingGroupModel.objects.get(
                            group_id=group_id, 
                            organization=request.user.organization
                        )
                    except MatchingGroupModel.DoesNotExist:
                        is_validate_correct = False
                        messages.error(request, UtilMessage.Validation.E_INVALID_ID.format("マッチンググループ"))
                
                if is_validate_correct and matching_group_obj:
                    if matching_group_obj.owner_account != request.user:
                        messages.error(request, UtilMessage.Browser.E_NOT_AUTHORIZED)
                        return redirect('app_matching:list')

                if is_validate_correct and matching_group_obj:
                    try:
                        # 削除
                        matching_group_obj.delete()
                        # メッセージ
                        messages.success(
                            request, 
                            UtilMessage.Database.S_DELETE.format(f"マッチンググループ（ID:{group_id}）")
                        )
                    except Exception as e:
                        # エラーメッセージ
                        messages.error(
                            request, 
                            UtilMessage.Database.E_DELETE.format(f"マッチンググループ（ID:{group_id}）")
                        )

            # ================
            # 検索処理場合
            # ================
            elif  button_action == "search":
                # バリデーション
                is_validate_correct = True

                # 検索文字列のバリデーション
                if search_keyword:
                    if not UtilValidation.is_length_valid(search_keyword, 1, 32):
                        is_validate_correct = False
                        messages.error(request, UtilMessage.Validation.E_PLZ_INP_LENGTH.format("検索文字列", 1, 32))
                    elif UtilValidation.has_special_characters(search_keyword):
                        is_validate_correct = False
                        messages.error(request, UtilMessage.Validation.E_INVALID_CHAR.format("検索文字列"))

                # バリデーションエラーのない場合
                if is_validate_correct:
                    # -------------------
                    # データ保存
                    # -------------------
                    # セッションに代入
                    self.request.session["matching_group_search_keyword"] = search_keyword

            # ==============================
            # ボタンアクションに該当がない場合
            # ==============================
            else:
                messages.error(request, UtilMessage.Browser.E_INVALID_REQUEST)

            # リダイレクト
            return redirect('app_matching:list')
        # ================
        # 例外処理:END
        # ================
        except Exception as e:
            # ログ出力
            logger.error(UtilMessage.Log.E_EXCEPT_POST.format(self.CLASS_LABEL, str(e)))
            # エラーレスポンスを返す
            return HttpResponseServerError(render(request, '500.html'))