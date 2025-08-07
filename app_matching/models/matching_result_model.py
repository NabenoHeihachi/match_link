from common.custom_base_model import CustomBaseModel
from django.db import models
from app_account.models.organization_model import OrganizationModel
from app_account.models.account_model import AccountModel
from app_matching.models.matching_group_model import MatchingGroupModel
from common.custom_validation_form import validate_no_dangerous_input

# ---------------------------
# マッチング結果テーブル
# 概要：マッチング結果情報を保持
# ----------------------------
class MatchingResultModel(CustomBaseModel):
    class MatchingMethod(models.TextChoices):
        HYBRID = 'hybrid', 'ハイブリッドマッチング'
        AUTO = 'auto', '自動マッチング'
        MANUAL = 'manual', '手動マッチング'

    # 結果ID
    result_id = models.AutoField(
            verbose_name="結果ID",
            db_column="RESULT_ID",
            primary_key=True,
        )
    
    # マッチンググループ
    matching_group = models.ForeignKey(
            MatchingGroupModel,
            verbose_name="マッチンググループ",
            db_column="MATCHING_GROUP",
            on_delete=models.CASCADE,
            related_name="matching_result_group",
            null=False,
            blank=False
        )
    
    # 所属組織
    organization = models.ForeignKey(
            OrganizationModel,
            verbose_name="所属組織",
            db_column="ORGANIZATION",
            on_delete=models.CASCADE,
            related_name="matching_result_organization",
            null=False,
            blank=False
        )
    
    # 投票者
    voter = models.ForeignKey(
            AccountModel,
            verbose_name="投票者",
            db_column="VOTER",
            on_delete=models.CASCADE,
            related_name="matching_result_voter",
            null=True,
            blank=True,
            default=None,
        )

    # 選ばれた人
    chosen_person = models.ForeignKey(
            AccountModel,
            verbose_name="選ばれた人",
            db_column="CHOSEN_PERSON",
            on_delete=models.CASCADE,
            related_name="matching_result_chosen",
            null=True,
            blank=True,
            default=None,
        )

    # マッチングスコア
    match_score = models.FloatField(
            verbose_name="マッチングスコア",
            db_column="MATCH_SCORE",
            null=True,
            blank=True,
            default=None,
    )

    # サマリー
    reason_summary = models.TextField(
            verbose_name="サマリー",
            db_column="REASON_SUMMARY",
            max_length=512,
            null=True,
            blank=True,
            default="",
            validators=[validate_no_dangerous_input],
    )

    # マッチング方法
    matching_method = models.CharField(
            verbose_name="マッチング方法",
            db_column="MATCHING_METHOD",
            max_length=64,
            choices=MatchingMethod.choices,
            default=MatchingMethod.HYBRID,
            null=False,
            blank=False,
            validators=[validate_no_dangerous_input],
            error_messages={
                'invalid': "有効なマッチング方法を選択してください。",
                'max_length': "マッチング方法は64文字以内で入力してください。"
            }
        )

    class Meta:
        db_table = 'MATCHING_RESULT'
        verbose_name = "マッチング結果"
        verbose_name_plural = "マッチング結果"
    
    def __str__(self):
        return f"マッチング結果 {self.result_id} - グループ: {self.matching_group.group_name}"