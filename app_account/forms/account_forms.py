from django import forms
from app_account.models.account_model import AccountModel
from app_account.models.organization_model import OrganizationModel
import re
from django.core.exceptions import ValidationError

def validate_password_complexity(value):
    if not value:
        return
    pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[!?()@])[A-Za-z\d!?()@]{8,256}$"
    if not re.match(pattern, value):
        raise ValidationError(
            "パスワードは英字・数字・記号（!?()@）をそれぞれ1つ以上含み、8〜256文字で構成してください。"
        )
    
class AccountSignupForm(forms.ModelForm):
    password = forms.CharField(
        label="パスワード*",
        widget=forms.PasswordInput(attrs={
            "label": "パスワード",
            "class": "form-control mb-3",
            "placeholder": "パスワードを入力してください。",
            "required": "required",
            "maxlength": "256"
        }),
        validators=[validate_password_complexity],
        min_length=8,
        max_length=256,
        error_messages={
            'label': "パスワード",
            'max_length': "パスワードは256文字以内で入力してください。",
            'min_length': "パスワードは8文字以上で入力してください。",
            'required': "パスワードは必須項目です。",
            'invalid': "パスワードは英字・数字・記号（!?()@）をそれぞれ1つ以上含み、8〜256文字で構成してください。"
        })
    
    password_confirm = forms.CharField(
        label="パスワード（確認用）*",
        widget=forms.PasswordInput(attrs={
            "class": "form-control mb-3",
            "placeholder": "もう一度パスワードを入力してください。",
            "required": "required",
            "maxlength": "256"
        })
    )
    
    class Meta:
        model = AccountModel
        fields = ['account_id', 'account_name', 'account_description', 'password', 'password_confirm']
        widgets = {
            'account_id': forms.TextInput(attrs={
                "class": "form-control mb-3",
                "placeholder": "例: User12345",
                "required": "required",
                "maxlength": "128"
            }),
            'account_name': forms.TextInput(attrs={
                "class": "form-control mb-3",
                "placeholder": "例: 管理太郎",
                "required": "required",
                "maxlength": "64"
            }),
            'account_description': forms.Textarea(attrs={
                'rows': 3,
                "class": "form-control mb-3",
                "placeholder": "アカウントの説明を入力してください。",
                "maxlength": "256"
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "パスワードが一致しません。")


class MemberCreateForm(AccountSignupForm):
    class Meta(AccountSignupForm.Meta):
        fields = ['account_id', 'account_name', 'account_description', 'password', 'password_confirm']

