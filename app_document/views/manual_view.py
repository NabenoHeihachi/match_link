# =================================
# マニュアル表示ビュー
# =================================
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.http import HttpResponseServerError, FileResponse
from common.util_message import UtilMessage
from django.conf import settings
import os
import logging

# ロガーの設定
logger = logging.getLogger(__name__)

class ManualView(TemplateView):
    # クラスラベル
    CLASS_LABEL = "マニュアル表示ビュー"

    def __init__(self):
        self.param = {

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
            # パラメータの取得  
            pdf_path = os.path.join(settings.MEDIA_ROOT, 'documents', 'manual.pdf')

            return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
        # ================
        # 例外処理:END
        # ================
        except FileNotFoundError:
            # メッセージ
            messages.error(request, UtilMessage.Browser.E_FILE_NOT_FOUND.format("マニュアル"))
            # リダイレクト
            return redirect('app_document:index')
        
        except Exception as e:
            # ログ出力
            logger.error(UtilMessage.Log.E_EXCEPT_GET.format(self.CLASS_LABEL, str(e)))
            # エラーレスポンスを返す
            return HttpResponseServerError(render(request, '500.html'))
