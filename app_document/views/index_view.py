from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from django.http import HttpResponseServerError
from common.util_message import UtilMessage
# ログ
import logging

# ロガーの設定
logger = logging.getLogger(__name__)

class IndexView(TemplateView):
    # クラスラベル
    CLASS_LABEL = "インデックスビュー"

    # テンプレートファイル
    template_name='app_document/index.html'

    def __init__(self):
        self.param = {}
    
    def get(self, request):
        """
        GET処理
        """
        # ================
        # 例外処理:START
        # ================
        try:
            # ログ出力
            logger.info(UtilMessage.Log.I_VIEW_GET.format(self.CLASS_LABEL))

            if request.user.is_authenticated:
                # ログインしている場合はリダイレクト
                return redirect('app_matching:list')

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
        
