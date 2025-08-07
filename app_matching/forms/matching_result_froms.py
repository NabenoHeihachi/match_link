from django import forms
from app_matching.models.matching_result_model import MatchingResultModel
from app_matching.models.matching_group_model import MatchingGroupModel

class MatchingResultManualForm(forms.ModelForm):
    class Meta:
        model = MatchingResultModel
        fields = ['chosen_person', 'reason_summary']
        widgets = {
            'chosen_person': forms.Select(attrs={
                "class": "form-select mb-3",
                "required": "required"
            }),
            'reason_summary': forms.Textarea(attrs={
                "class": "form-control mb-3",
                "placeholder": "選んだ理由を入力してください",
                "rows": 3,
                "maxlength": "256"
            }),
        }

    def __init__(self, *args, group_id, **kwargs):
        super().__init__(*args, **kwargs)

        group = MatchingGroupModel.objects.get(group_id=group_id)
        self.fields['chosen_person'].queryset = group.matching_candidates.all()

class MatchingResultSelectMethodForm(forms.ModelForm):
    class Meta:
        model = MatchingResultModel
        fields = ['matching_method']
        widgets = {
            'matching_method': forms.Select(attrs={
                "class": "form-select mb-3",
                "required": "required",
                "id": "floatingSelect",
                "placeholder": "マッチング方式を選択してください",
                "aria-label": "マッチング方式選択",
            }),
        }
