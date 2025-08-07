from django.db import models
from common.custom_base_model import CustomBaseModel
from app_account.models.subscription_model import SubscriptionModel
from common.custom_validation_form import validate_no_dangerous_input
import uuid

# ---------------------------
# 支払い履歴テーブル
# 概要：支払い履歴情報を保持
# ----------------------------
class PaymentHistoryModel(CustomBaseModel):
    class PaymentMethod(models.TextChoices):
        CREDIT_CARD = 'credit_card', 'クレジットカード'
        BANK_TRANSFER = 'bank_transfer', '銀行振込'
        OTHER = 'other', 'その他'
        
    class PaymentStatus(models.TextChoices):
        PAID = 'paid', '支払い済み'
        PENDING = 'pending', '未処理'
        FAILED = 'failed', '失敗'
        REFUNDED = 'refunded', '返金済み'

    # ID
    id = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            editable=False,
            verbose_name="ID",
            db_column="ID"
        )
    
    # 組織ID
    organization_id = models.CharField(
            max_length=255,
            verbose_name="組織ID",
            db_column="ORGANIZATION_ID",
            validators=[validate_no_dangerous_input],
        )

    # 組織名
    organization_name = models.CharField(
            verbose_name="組織名",
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
    
    # 支払い名義
    payment_name = models.CharField(
            verbose_name="支払い名義",
            db_column="PAYMENT_NAME",
            max_length=256,
            null=False,
            blank=False,
            validators=[validate_no_dangerous_input],
            error_messages={
                'invalid': "有効な支払い名義を入力してください。",
                'max_length': "支払い名義は64文字以内で入力してください。"
            }
        )
    
    # 支払い金額
    payment_amount = models.DecimalField(
            verbose_name="支払い金額",
            db_column="PAYMENT_AMOUNT",
            max_digits=10,
            decimal_places=2,
            null=False,
            blank=False,
            error_messages={
                'invalid': "有効な支払い金額を入力してください。",
                'max_digits': "支払い金額は10桁以内で入力してください。",
                'decimal_places': "支払い金額は小数点以下2桁まで入力してください。"
            }
        )
    
    # サブスクリプション
    subscription = models.ForeignKey(
            SubscriptionModel,
            verbose_name="サブスクリプション",
            db_column="SUBSCRIPTION",
            on_delete=models.PROTECT,
            null=False,
            blank=False,
            related_name='payment_histories'
        )
    

    # 決済サービスの取引IDなど
    transaction_id = models.CharField(
            verbose_name="取引ID",
            db_column="TRANSACTION_ID",
            max_length=128,
            null=True,
            blank=True,
            default="",
            validators=[validate_no_dangerous_input],
            error_messages={
                'invalid': "有効な取引IDを入力してください。",
                'max_length': "取引IDは128文字以内で入力してください。"
            }
        )
    
    # 支払日時
    payment_date = models.DateTimeField(
            verbose_name="支払日時",
            db_column="PAYMENT_DATE",
            null=False,
            blank=False
        )

    # 開始日
    start_date = models.DateTimeField(
            verbose_name="開始日",
            db_column="START_DATE",
            null=False,
            blank=False
        )

    # 有効期限
    expiration_date = models.DateTimeField(
            verbose_name="有効期限",
            db_column="EXPIRATION_DATE",
            null=False,
            blank=False
        )
    

    # 支払い方法
    payment_method = models.CharField(
            verbose_name="支払い方法",
            db_column="PAYMENT_METHOD",
            max_length=20,
            choices=PaymentMethod.choices,
            default=PaymentMethod.CREDIT_CARD,
            null=False,
            blank=False
        )
    
    payment_status = models.CharField(
            verbose_name="支払いステータス",
            db_column="PAYMENT_STATUS",
            max_length=20,
            choices=PaymentStatus.choices,
            default=PaymentStatus.PENDING,
            null=False,
            blank=False
        )

    class Meta:
            db_table = "PAYMENTHISTORY_MODEL"
            verbose_name = '支払い履歴'
            verbose_name_plural = '支払い履歴'

    def __str__(self):
        return f"{self.organization_name} - {self.subscription.subscription_name} - {self.payment_amount}円"