from django import forms
from app_profile.models.personality_model import PersonalityModel

class PersonalityTagForm(forms.ModelForm):
    class Meta:
        model = PersonalityModel
        fields = [
            'value_tags',
            'hobby_tags',
            'communication_tags',
        ]
        widgets = {
            'value_tags': forms.CheckboxSelectMultiple(
                attrs={'class': 'form-check-input'}
            ),
            'hobby_tags': forms.CheckboxSelectMultiple(
                attrs={'class': 'form-check-input'}
            ),
            'communication_tags': forms.CheckboxSelectMultiple(
                attrs={'class': 'form-check-input'}
            ),
        }


class BigFiveSurveyForm(forms.Form):
    CHOICES = [
        (1, '全くそう思わない'),
        (2, 'あまりそう思わない'),
        (3, 'どちらとも言えない'),
        (4, 'ややそう思う'),
        (5, 'とてもそう思う'),
    ]

    # 外向性
    ex_q1 = forms.ChoiceField(label="プレゼンなど人前で話すことにワクワクする", choices=CHOICES, widget=forms.RadioSelect(
        attrs={'class': 'form-check-input', 'required': 'required'}
    ))
    ex_q2 = forms.ChoiceField(label="座談会など初対面の人とでもすぐに打ち解ける", choices=CHOICES, widget=forms.RadioSelect(
        attrs={'class': 'form-check-input', 'required': 'required'}
    ))
    ex_q3 = forms.ChoiceField(label="一人の時間よりも、誰かと過ごす時間を好む", choices=CHOICES, widget=forms.RadioSelect(
        attrs={'class': 'form-check-input', 'required': 'required'}
    ))

    # 情緒安定性
    ne_q1 = forms.ChoiceField(label="プレッシャーがかかっても、冷静さを保てる", choices=CHOICES, widget=forms.RadioSelect(
        attrs={'class': 'form-check-input', 'required': 'required'}
    ))
    ne_q2 = forms.ChoiceField(label="小さなことでクヨクヨすることは少ない", choices=CHOICES, widget=forms.RadioSelect(
        attrs={'class': 'form-check-input', 'required': 'required'}
    ))
    ne_q3 = forms.ChoiceField(label="失敗してもすぐに気持ちを切り替えられる", choices=CHOICES, widget=forms.RadioSelect(
        attrs={'class': 'form-check-input', 'required': 'required'}
    ))

    # 開放性
    op_q1 = forms.ChoiceField(label="新しい体験やアイデアに触れることが好きだ", choices=CHOICES, widget=forms.RadioSelect(
        attrs={'class': 'form-check-input', 'required': 'required'}
    ))
    op_q2 = forms.ChoiceField(label="芸術や音楽など、感性を刺激するものに興味がある", choices=CHOICES, widget=forms.RadioSelect(
        attrs={'class': 'form-check-input', 'required': 'required'}
    ))
    op_q3 = forms.ChoiceField(label="慣れないことにもチャレンジしたいと思う", choices=CHOICES, widget=forms.RadioSelect(
        attrs={'class': 'form-check-input', 'required': 'required'}
    ))

    # 協調性
    ag_q1 = forms.ChoiceField(label="困っている人を見ると、自然と手助けしたくなる", choices=CHOICES, widget=forms.RadioSelect(
        attrs={'class': 'form-check-input', 'required': 'required'}
    ))
    ag_q2 = forms.ChoiceField(label="人の話をよく聞き、共感する方だと思う", choices=CHOICES, widget=forms.RadioSelect(
        attrs={'class': 'form-check-input', 'required': 'required'}
    ))
    ag_q3 = forms.ChoiceField(label="周囲との衝突はできるだけ避けたいと思う", choices=CHOICES, widget=forms.RadioSelect(
        attrs={'class': 'form-check-input', 'required': 'required'}
    ))

    # 誠実性
    co_q1 = forms.ChoiceField(label="一度決めたことは、最後までやり遂げる", choices=CHOICES, widget=forms.RadioSelect(
        attrs={'class': 'form-check-input', 'required': 'required'}
    ))
    co_q2 = forms.ChoiceField(label="スケジュールや計画を立てて行動するのが好きだ", choices=CHOICES, widget=forms.RadioSelect(
        attrs={'class': 'form-check-input', 'required': 'required'}
    ))
    co_q3 = forms.ChoiceField(label="忘れ物や遅刻はできるだけしないようにしている", choices=CHOICES, widget=forms.RadioSelect(
        attrs={'class': 'form-check-input', 'required': 'required'}
    ))