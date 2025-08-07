from django.db import models

class CustomBaseModel(models.Model):
    # 論理削除フラグ
    is_deleted = models.BooleanField(
            verbose_name="削除フラグ", 
            db_column="IS_DELETED", 
            null=False, 
            blank=False,
            default=False
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
            max_length=256,
            null=True,
            blank=True,
            default=""
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
            max_length=256,
            null=True,
            blank=True,
            default=""
        )
    
    class Meta:
        abstract = True