from django import forms
from app_profile.models.profile_model import ProfileModel

class ProfileImageForm(forms.ModelForm):
    profile_image = forms.ChoiceField(
        label="プロフィール画像",
        choices=ProfileModel.PROFILE_IMAGE_CHOICES,
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
            'required': 'required'
        }),
        error_messages={
            'required': "プロフィール画像は必須項目です。"
        }
    )
    class Meta:
        model = ProfileModel
        fields = ['profile_image']

class ProfileInputForm(forms.ModelForm):
    class Meta:
        model = ProfileModel
        fields = [
            "position",
            "age",
            "self_introduction", 
            "final_education", 
            "preferred_partner_description", 
            "special_skills"
        ]
        widgets = {
            'position': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    "placeholder": "例: ソフトウェアエンジニア",
                    "maxlength": "256"
                }
            ),
            'age': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    "placeholder": "例: 30",
                    "min": "0",
                    "max": "120"
                }
            ),
            'self_introduction': forms.Textarea(
                attrs={
                    'class': 'form-control', 
                    "placeholder": "例: 私はチームワークを大切にし、常に学び続ける姿勢を持っています。趣味は読書とハイキングで、特に歴史小説が好きです。",
                    "maxlength": "256",
                    'rows': 3
                    }
            ),
            'final_education': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    "placeholder": "例: ML大学 ML学部 ML学科",
                    "maxlength": "256"
                }
            ),
            'preferred_partner_description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    "placeholder": "例: チームワークを重視し、コミュニケーション能力が高い方と一緒に働きたいです。",
                    "maxlength": "256",
                    'rows': 3
                }
            ),
            'special_skills': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    "placeholder": "例: Pythonプログラミング、データ分析、プロジェクト管理",
                    "maxlength": "256",
                    'rows': 3
                }
            ),
        }
