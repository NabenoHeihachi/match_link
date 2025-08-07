from django.contrib import admin
from app_matching.models.matching_group_model import MatchingGroupModel
from app_matching.models.matching_result_model import MatchingResultModel

class MatchingGroupModelAdmin(admin.ModelAdmin):
    """
    管理画面用のマッチンググループモデル管理クラス
    """
    list_display = ('group_id', 'group_name', 'owner_account__account_id', 'matching_type')
    search_fields = ('group_name', 'owner_account__account_id')
    list_filter = ('matching_type',)
    ordering = ('-created_at',)


class MatchingResultModelAdmin(admin.ModelAdmin):
    """
    管理画面用のマッチング結果モデル管理クラス
    """
    list_display = ('result_id', 'matching_group__group_name')
    search_fields = ('matching_group__group_name',)
    list_filter = ('matching_group__organization',)
    ordering = ('-created_at',)


# 管理画面にマッチンググループモデルを登録
admin.site.register(MatchingGroupModel, MatchingGroupModelAdmin)

# 管理画面にマッチング結果モデルを登録
admin.site.register(MatchingResultModel, MatchingResultModelAdmin)
