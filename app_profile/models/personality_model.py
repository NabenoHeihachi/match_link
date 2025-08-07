from common.custom_base_model import CustomBaseModel
from django.db import models
from app_account.models.account_model import AccountModel
from app_account.models.organization_model import OrganizationModel
from app_profile.models.options_model import ValueTagModel, HobbyTagModel, CommunicationTagModel

class PersonalityModel(CustomBaseModel):
    account = models.OneToOneField(
        AccountModel,
        verbose_name="アカウント",
        db_column="ACCOUNT",
        on_delete=models.CASCADE,
        related_name="personality_account",
        null=False,
        blank=False,
    )

    organization = models.ForeignKey(
        OrganizationModel,
        verbose_name="組織",
        db_column="ORGANIZATION",
        on_delete=models.CASCADE,
        related_name="personality_organization",
        null=False,
        blank=False,
    )

    big_five_extraversion = models.IntegerField(
        verbose_name="ビッグファイブ・外向性",
        db_column="BIG_FIVE_Extraversion",
        null=False,
        blank=False,
    )

    big_five_neuroticism = models.IntegerField(
        verbose_name="ビッグファイブ・情緒安定性",
        db_column="BIG_FIVE_Neuroticism",
        null=False,
        blank=False,
    )

    big_five_openness = models.IntegerField(
        verbose_name="ビッグファイブ・開放性",
        db_column="BIG_FIVE_Openness",
        null=False,
        blank=False,
    )

    big_five_agreeableness = models.IntegerField(
        verbose_name="ビッグファイブ・協調性",
        db_column="BIG_FIVE_Agreeableness",
        null=False,
        blank=False,
    )

    big_five_conscientiousness = models.IntegerField(
        verbose_name="ビッグファイブ・誠実性",
        db_column="BIG_FIVE_Conscientiousness",
        null=False,
        blank=False,
    )


    hobby_tags = models.ManyToManyField(
        HobbyTagModel,
        verbose_name="趣味タグ",
        db_column="HOBBY_TAGS",
        related_name="personality_hobby_tags",
        blank=True,
    )

    value_tags = models.ManyToManyField(
        ValueTagModel,
        verbose_name="価値観タグ",
        db_column="VALUE_TAGS",
        related_name="personality_value_tags",
        blank=True,
    )

    communication_tags = models.ManyToManyField(
        CommunicationTagModel,
        verbose_name="コミュニケーションタグ",
        db_column="COMMUNICATION_TAGS",
        related_name="personality_communication_tags",
        blank=True,
    )

    class Meta:
        db_table = "PERSONALITY"
        verbose_name = "パーソナリティ"
        verbose_name_plural = "パーソナリティ一覧"

    def __str__(self):
        return f"Personality of {self.account.account_id} in {self.organization.organization_id}"
