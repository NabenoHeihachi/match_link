from django import forms
from app_account.models.paymenthistory_model import PaymentHistoryModel

class PaymentHistoryCreateForm(forms.ModelForm):
    class Meta:
        model = PaymentHistoryModel
        fields = ['payment_name', 'payment_date', 'start_date', 'expiration_date']
        widgets = {
            "payment_name": forms.TextInput(attrs={
                "class": "form-control mb-3",
                "placeholder": "例: 支払太郎",
                "required": "required",
                "maxlength": "256"
            }),
            "payment_date": forms.DateTimeInput(attrs={
                "type": "datetime-local",
                "class": "form-control mb-3",
                "placeholder": "例: 2023-01-01 12:00",
            }),
            "start_date": forms.DateTimeInput(attrs={
                "type": "datetime-local",
                "class": "form-control mb-3",
                "placeholder": "例: 2023-01-01 12:00",
            }),
            "expiration_date": forms.DateTimeInput(attrs={
                "type": "datetime-local",
                "class": "form-control mb-3",
                "placeholder": "例: 2023-01-01 12:00",
            }),
        }