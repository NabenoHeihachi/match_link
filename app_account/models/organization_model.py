from common.custom_base_model import CustomBaseModel
from django.db import models
from app_account.models.subscription_model import SubscriptionModel
from common.custom_validation_form import validate_no_dangerous_input

# ---------------------------
# 組織テーブル
# 概要：組織情報を保持
# ----------------------------
class OrganizationModel(CustomBaseModel):
    # 組織ID
    organization_id = models.AutoField(
            verbose_name="組織ID",
            db_column="ORGANIZATION_ID",
            primary_key=True,
        )
    
    # 組織名
    organization_name = models.CharField(
            verbose_name="組織名*",
            db_column="ORGANIZATION_NAME",
            max_length=64,
            null=False,
            blank=False,
            validators=[validate_no_dangerous_input],
            error_messages={
                'invalid': "有効な組織名を入力してください。",
                'max_length': "組織名は64文字以内で入力してください。"
            }
        )   
    
    # 組織説明
    organization_description = models.TextField(
            verbose_name="組織説明",
            db_column="ORGANIZATION_DESCRIPTION",
            max_length=256,
            default="",
            null=True,
            blank=True,
            validators=[validate_no_dangerous_input],
            error_messages={
                'invalid': "有効な組織説明を入力してください。",
                'blank': "組織説明は必須項目です。",
                'max_length': "組織説明は256文字以内で入力してください。"
            }
        )  

    # 組織EMAIL
    organization_email = models.EmailField(
            verbose_name="組織EMAIL",
            db_column="ORGANIZATION_EMAIL",
            max_length=254,
            null=True,
            blank=True,
            default="",
            validators=[validate_no_dangerous_input],
            error_messages={
                'unique': "この組織EMAILはすでに使用されています。",
                'invalid': "有効な組織EMAILを入力してください。",
                'max_length': "組織EMAILは254文字以内で入力してください。"
            }
        )
    
    # 支払い済みフラグ
    is_paid = models.BooleanField(
            verbose_name="支払い済みフラグ",
            db_column="IS_PAID",
            default=False,
            null=False,
            blank=False
        )
    
    # メールチェックフラグ
    is_email_checked = models.BooleanField(
            verbose_name="メールチェックフラグ",
            db_column="IS_EMAIL_CHECKED",
            default=False,
            null=False,
            blank=False,
    )
    
    # 組織サブスクリプション
    subscription = models.ForeignKey(
            SubscriptionModel,
            verbose_name="サブスクリプション",
            db_column="SUBSCRIPTION_ID",
            on_delete=models.SET_NULL,
            default=None,
            null=True,
            blank=True,
            related_name="organizations_subscription"
        )
    

    # テーブル名
    class Meta:
        db_table = "ORGANIZATION_MODEL"
        verbose_name = "組織"
        verbose_name_plural = "組織一覧"

    def __str__(self):
        return self.organization_name
    