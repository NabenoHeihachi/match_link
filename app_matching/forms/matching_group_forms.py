from django import forms
from app_matching.models.matching_group_model import MatchingGroupModel
from app_account.models.account_model import AccountModel

class MatchingGroupInputForm(forms.ModelForm):
    class Meta:
        model = MatchingGroupModel
        fields = ['group_name', 'group_description', 'matching_type', 'target_user']
        widgets = {
            "group_name": forms.TextInput(attrs={
                "class": "form-control mb-3",
                "placeholder": "例: マッチンググループ",
                "required": "required",
                "maxlength": "64"
            }),
            "group_description": forms.Textarea(attrs={
                "class": "form-control mb-3",
                "placeholder": "グループの説明を入力してください",
                "rows": 3,
                "maxlength": "256"
            }),
            "matching_type": forms.Select(attrs={
                "class": "form-select mb-3",
                "required": "required"
            }),
            "target_user": forms.Select(attrs={
                "class": "form-select mb-3",
                "required": "required"
            })
            
        }
    
    def __init__(self, *args, organization, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['target_user'].queryset = AccountModel.objects.filter(
            organization=organization,
            is_setup_completed=True
            ).order_by('account_name')

class MatchingGroupCandidatesForm(forms.ModelForm):
    class Meta:
        model = MatchingGroupModel
        fields = ['matching_candidates']
        widgets = {
            'matching_candidates': forms.CheckboxSelectMultiple(attrs={
                "class": "form-check-input mb-1",
            }),
        }

    def __init__(self, *args, organization, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['matching_candidates'].queryset = AccountModel.objects.filter(
            organization=organization,
            is_setup_completed=True
            ).order_by('account_name')
    
    def clean_matching_candidates(self):
        selected = self.cleaned_data.get('matching_candidates')
        if selected is None or len(selected) < 2:
            raise forms.ValidationError("最低でも2人以上の候補者を選択してください。")
        return selected
