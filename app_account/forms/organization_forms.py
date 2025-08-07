from django import forms
from app_account.models.organization_model import OrganizationModel

class OrganizationSignupForm(forms.ModelForm):
    class Meta:
        model = OrganizationModel
        fields = ['organization_name', 'organization_description', 'organization_email']
        widgets = {
            "organization_name": forms.TextInput(attrs={
                "class": "form-control mb-3",
                "placeholder": "例: 株式会社サンプル",
                "required": "required",
                "maxlength": "100"
            }),
            'organization_description': forms.Textarea(attrs={
                'rows': 3,
                "class": "form-control mb-3",
                "placeholder": "例: 教育系スタートアップ企業",
                "maxlength": "255"
                }),
            'organization_email': forms.EmailInput(attrs={
                "class": "form-control mb-3",
                "placeholder": "例: info@example.com",
                "maxlength": "100",
            }),
        }

class OrganizationUpdateForm(OrganizationSignupForm):
    pass