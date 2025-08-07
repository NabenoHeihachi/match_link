from common.custom_base_model import CustomBaseModel
from django.db import models
from common.custom_validation_form import validate_no_dangerous_input

# ---------------------------
# サブスクリプションテーブル
# 概要：サブスクリプション情報を保持
# ----------------------------
class SubscriptionModel(CustomBaseModel):
    # サブスクリプションID
    subscription_id = models.AutoField(
            verbose_name="サブスクリプションID",
            db_column="SUBSCRIPTION_ID",
            primary_key=True
        )
    
    # サブスクリプション名
    subscription_name = models.CharField(
            verbose_name="サブスクリプション名",
            db_column="SUBSCRIPTION_NAME",
            max_length=64,
            unique=True,
            null=False,
            blank=False,
            validators=[validate_no_dangerous_input],
        )
    
    # サブスクリプションタイトル
    subscription_title = models.CharField(
            verbose_name="サブスクリプションタイトル",
            db_column="SUBSCRIPTION_TITLE",
            max_length=64,
            default="",
            null=True,
            blank=True,
            validators=[validate_no_dangerous_input],
        )
    
    # サブスクリプション説明
    subscription_description = models.TextField(
            verbose_name="サブスクリプション説明",
            db_column="SUBSCRIPTION_DESCRIPTION",
            max_length=256,
            default="",
            null=True,
            blank=True,
            validators=[validate_no_dangerous_input],
        )
    
    # サブスクリプション価格
    subscription_price = models.IntegerField(
            verbose_name="サブスクリプション価格",
            db_column="SUBSCRIPTION_PRICE",
            null=False,
            blank=False,
        )   
    
    # アカウント作成可能数
    account_limit = models.IntegerField(
            verbose_name="アカウント作成可能数",
            db_column="ACCOUNT_LIMIT",
            default=10,
            null=False,
            blank=False
        )
    
    # マッチンググループ作成数
    matching_group_limit = models.IntegerField(
            verbose_name="マッチンググループ作成数",
            db_column="MATCHING_GROUP_LIMIT",
            default=2,
            null=False,
            blank=False
        )
    
    # AI利用フラグ
    is_ai_enabled = models.BooleanField(
            verbose_name="AI利用フラグ",
            db_column="IS_AI_ENABLED",
            default=False,
            null=False,
            blank=False
        )
    
    # テーブル名
    class Meta:
        db_table = "SUBSCRIPTION_MODEL"
        verbose_name = "サブスクリプション"
        verbose_name_plural = "サブスクリプション一覧"

    def __str__(self):
        return self.subscription_name