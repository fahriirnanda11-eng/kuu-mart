from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):

    class Meta:
        model = ContactMessage

        fields = [
            "nama",
            "email",
            "pesan",
        ]

        widgets = {

            "nama": forms.TextInput(
                attrs={
                    "placeholder": "Nama lengkap"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Email"
                }
            ),

            "pesan": forms.Textarea(
                attrs={
                    "placeholder": "Tulis pesan Anda...",
                    "rows": 5
                }
            ),
        }