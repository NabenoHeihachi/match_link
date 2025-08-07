from common.custom_base_model import CustomBaseModel
from django.db import models
from common.custom_validation_form import validate_no_dangerous_input
from app_account.models.account_model import AccountModel
from app_account.models.organization_model import OrganizationModel

class ProfileModel(CustomBaseModel):
    PROFILE_IMAGE_CHOICES = [
        ('img/profile/default1_m.jpeg', '男性１'),
        ('img/profile/default2_m.jpeg', '男性２'),
        ('img/profile/default3_m.jpeg', '男性３'),
        ('img/profile/default4_m.jpeg', '男性４'),
        ('img/profile/default1_w.jpeg', '女性１'),
        ('img/profile/default2_w.jpeg', '女性２'),
        ('img/profile/default3_w.jpeg', '女性３'),
        ('img/profile/default4_w.jpeg', '女性４'),
    ]

    account = models.OneToOneField(
        AccountModel,
        verbose_name="アカウント",
        db_column="ACCOUNT",
        on_delete=models.CASCADE,
        related_name="profile_account",
        null=False,
        blank=False,
    )

    organization = models.ForeignKey(
        OrganizationModel,
        verbose_name="組織",
        db_column="ORGANIZATION",
        on_delete=models.CASCADE,
        related_name="profile_organization",
        null=False,
        blank=False,
    )

    age = models.IntegerField(
        verbose_name="年齢",
        db_column="AGE",
        null=True,
        blank=True,
        default=None,
    )

    position = models.CharField(
        verbose_name="役職・所属",
        db_column="POSITION",
        max_length=64,
        null=True,
        blank=True,
        default="",
        validators=[validate_no_dangerous_input]
    )

    profile_image = models.CharField(
        verbose_name="プロフィール画像",
        db_column="PROFILE_IMAGE",
        max_length=256,
        choices=PROFILE_IMAGE_CHOICES,
        default='img/profile/default1_m.jpeg',
        null=False,
        blank=False,
    )

    self_introduction = models.TextField(
        verbose_name="自己紹介",
        db_column="SELF_INTRODUCTION",
        max_length=256,
        null=True,
        blank=True,
        default="",
        validators=[validate_no_dangerous_input]
    )

    final_education = models.CharField(
        verbose_name="最終学歴",
        db_column="FINAL_EDUCATION",
        max_length=256,
        null=True,
        blank=True,
        default="",
        validators=[validate_no_dangerous_input]
    )

    preferred_partner_description = models.TextField(
        verbose_name="一緒に働きたい人物像",
        db_column="PREFERRED_PARTNER_DESCRIPTION",
        max_length=256,
        null=True,
        blank=True,
        default="",
        validators=[validate_no_dangerous_input]
    )

    special_skills = models.TextField(
        verbose_name="特技・スキル",
        db_column="SPECIAL_SKILLS",
        max_length=256,
        null=True,
        blank=True,
        default="",
        validators=[validate_no_dangerous_input]
    )

    class Meta:
        db_table = "PROFILE"
        verbose_name = "プロフィール"
        verbose_name_plural = "プロフィール一覧"

    def __str__(self):
        return f"Profile of {self.account.account_id} in {self.organization.organization_id}"