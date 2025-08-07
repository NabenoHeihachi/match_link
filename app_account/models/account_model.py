from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from common.util_authority import UtilAuthority
from common.custom_validation_form import validate_no_dangerous_input
import uuid
from app_account.models.organization_model import OrganizationModel

# ---------------------------
# アカウントテーブル
# 概要：システムアカウント情報を保持
# ----------------------------
class AccountModel(AbstractUser):
    username = None
    last_name = None
    first_name = None
    email = None

    # ID
    id = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            editable=False,
            verbose_name="ID",
            db_column="ID"
        )

    # アカウントID
    account_id = models.CharField(
            verbose_name="アカウントID*",
            db_column="ACCOUNT_ID",
            max_length=128, 
            unique=True, 
            null=False,
            blank=False,
            validators=[RegexValidator(r'^[A-Za-z0-9]{8,128}$')],
            error_messages={
                'unique': "このアカウントIDはすでに使用されています。",
                'invalid': "有効なアカウントIDを入力してください。（半角英数字8文字以上128文字以内）"
            }
        )
    
    # アカウント名前
    account_name = models.CharField(
            verbose_name="アカウント名前*",
            db_column="ACCOUNT_NAME",
            max_length=64, 
            null=False,
            blank=False,
            validators=[validate_no_dangerous_input],
            error_messages={
                'invalid': "利用できない文字が含まれています。",
                'max_length': "アカウント名前は64文字以内で入力してください。"
            }
        )
    
    # アカウント説明
    account_description = models.TextField(
            verbose_name="アカウント説明",
            db_column="ACCOUNT_DESCRIPTION",
            max_length=256,
            default="",
            null=True,
            blank=True,
            validators=[validate_no_dangerous_input],
            error_messages={
                'invalid': "利用できない文字が含まれています。",
                'blank': "アカウント説明は必須項目です。",
                'max_length': "アカウント説明は256文字以内で入力してください。"

            }
        )


    # 権限コード
    auth_code = models.CharField(
            verbose_name="権限コード",
            db_column="AUTH_CODE",
            choices= UtilAuthority.get_reversed_dict(),
            max_length=32, 
            null=False,
            blank=False,
        )
    
    # 組織
    organization = models.ForeignKey(
            OrganizationModel,
            verbose_name="組織",
            db_column="ORGANIZATION_ID",
            related_name="accounts_organization",
            editable=False,
            on_delete=models.CASCADE,
            null=False,
            blank=False,
        )
    
    # メンバー番号
    member_number = models.IntegerField(
            verbose_name="メンバー番号",
            db_column="MEMBER_NUMBER",
            default=0,
            null=False,
            blank=False,
    )

    # 作成時刻
    created_at = models.DateTimeField(
            verbose_name="作成時刻",
            db_column="CREATED_AT",
            auto_now_add=True,
            null=False, 
            blank=False
        )
    
    # 作成者
    created_by = models.CharField(
            verbose_name="作成者",
            db_column="CREATED_BY",
            max_length=128,
            null=False,
            blank=False
        )
    
    # 更新時刻
    updated_at = models.DateTimeField(
            verbose_name="更新時刻",
            db_column="UPDATED_AT",
            auto_now=True, 
            null=True,
            blank=False
        )
    
    # 更新者
    updated_by = models.CharField(
            verbose_name="更新者",
            db_column="UPDATED_BY",
            max_length=128,
            null=True,
            blank=False
        )
    
    is_staff = models.BooleanField(
        default=False,
        )
    is_superuser = models.BooleanField(
        default=False,
    )

    is_setup_completed = models.BooleanField(
        verbose_name="セットアップ完了フラグ",
        db_column="IS_SETUP_COMPLETED",
        default=False,
        null=False,
        blank=False,
    )

    USERNAME_FIELD = "account_id"
    REQUIRED_FIELDS = []

    # テーブル名
    class Meta:
        db_table = "ACCOUNT_MODEL"
        verbose_name = "アカウント"
        verbose_name_plural = "アカウント一覧"
    
    def __str__(self):
        return f"{self.account_name} (ID:{self.member_number})"
