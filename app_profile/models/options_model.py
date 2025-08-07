from common.custom_base_model import CustomBaseModel
from django.db import models
from common.custom_validation_form import validate_no_dangerous_input

class OptionsBaseModel(CustomBaseModel):
    tag_name = models.CharField(
        verbose_name="タグ",
        db_column="TAG",
        max_length=64,
        null=False,
        blank=False,
        unique=True,
        validators=[validate_no_dangerous_input]
        )
    
    class Meta:
        abstract = True
    
    def __str__(self):
        return self.tag_name

class ValueTagModel(OptionsBaseModel):
    class Meta:
        db_table = "VALUE_TAG"
        verbose_name = "価値観タグ"
        verbose_name_plural = "価値観タグ一覧"

class HobbyTagModel(OptionsBaseModel):
    class Meta:
        db_table = "HOBBY_TAG"
        verbose_name = "趣味タグ"
        verbose_name_plural = "趣味タグ一覧"


class CommunicationTagModel(OptionsBaseModel):
    class Meta:
        db_table = "COMMUNICATION_TAG"
        verbose_name = "コミュニケーションタグ"
        verbose_name_plural = "コミュニケーションタグ一覧"