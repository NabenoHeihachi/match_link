from common.custom_base_model import CustomBaseModel
from django.db import models
from app_account.models.organization_model import OrganizationModel
from app_account.models.account_model import AccountModel
from common.custom_validation_form import validate_no_dangerous_input

# ---------------------------
# マッチンググループテーブル
# 概要：マッチンググループ情報を保持
# ----------------------------
class MatchingGroupModel(CustomBaseModel):
    class MatchingType(models.TextChoices):
        SUPERVISOR_MATCHING = 'supervisor_matching', '上司マッチング'
        SUBORDINATE_MATCHING = 'subordinate_matching', '部下マッチング'
        PEER_MATCHING = 'peer_matching', 'ペアマッチング'

    # グループID
    group_id = models.AutoField(
            verbose_name="グループID",
            db_column="GROUP_ID",
            primary_key=True,
        )
    
    # グループ名
    group_name = models.CharField(
            verbose_name="グループ名",
            db_column="GROUP_NAME",
            max_length=64,
            null=False,
            blank=False,
            validators=[validate_no_dangerous_input],
            error_messages={
                'invalid': "有効なグループ名を入力してください。",
                'max_length': "グループ名は64文字以内で入力してください。"
            }
        )
    
    # グループ説明
    group_description = models.TextField(
            verbose_name="グループ説明",
            db_column="GROUP_DESCRIPTION",
            max_length=256,
            null=True,
            blank=True,
            default="",
            validators=[validate_no_dangerous_input],
            error_messages={
                'invalid': "有効なグループ説明を入力してください。",
                'max_length': "グループ説明は256文字以内で入力してください。"
            }
        )

    # オーナーアカウントID
    owner_account = models.ForeignKey(
            AccountModel,
            verbose_name="オーナーアカウント",
            db_column="OWNER_ACCOUNT",
            on_delete=models.CASCADE,
            related_name="matching_group_owner",
            null=False,
            blank=False
        )
    
    # 所属組織
    organization = models.ForeignKey(
            OrganizationModel,
            verbose_name="所属組織",
            db_column="ORGANIZATION",
            on_delete=models.CASCADE,
            related_name="matching_group_organization",
            null=False,
            blank=False
        )
    
    # マッチングタイプ
    matching_type = models.CharField(
            max_length=32,
            choices=MatchingType.choices,
            default=MatchingType.SUPERVISOR_MATCHING,
            verbose_name="マッチングタイプ",
            db_column="MATCHING_TYPE",
            null=False,
            blank=False,
            validators=[validate_no_dangerous_input],
            error_messages={
                'invalid': "有効なマッチングタイプを選択してください。",
                'max_length': "マッチングタイプは32文字以内で入力してください。"
            }
        )
    
    # マッチング完了フラグ
    is_matching_completed = models.BooleanField(
            verbose_name="マッチング完了フラグ",
            db_column="IS_MATCHING_COMPLETED",
            default=False,
        )

    # 対象者
    target_user = models.ForeignKey(
            AccountModel,
            verbose_name="対象者",
            db_column="TARGET_USER",
            related_name="matching_group_target_user",
            blank=False,
            null=False,
            on_delete=models.CASCADE
        )
    
    # マッチング候補者
    matching_candidates = models.ManyToManyField(
            AccountModel,
            verbose_name="マッチング候補者",
            db_column="MATCHING_CANDIDATES",
            related_name="matching_group_candidates",
            blank=True,
        )
    
    class Meta:
        db_table = "MATCHING_GROUP_MODEL"
        verbose_name = "マッチンググループ"
        verbose_name_plural = "マッチンググループ"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.group_name} ({self.group_id}) - {self.organization.organization_name}"