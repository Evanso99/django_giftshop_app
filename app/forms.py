from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import CustomUser




class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True
    )
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    security_question = forms.CharField(
        label=_("Security Question"), 
        help_text=_("Which city was your mother born?"), 
        required=True
    )

    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'security_question', 'first_name', 'last_name', )
    


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser  
        fields = ['username', 'email', 'first_name', 'last_name']  


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'autofocus': True})
    )
    security_answer = forms.CharField(
        label=_("Security Answer"), 
        max_length=100, 
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )

    error_messages = {
        'invalid_email': _("The email address is not associated with any account."),
        'invalid_security_answer': _("The security answer is incorrect."),
    }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        User = CustomUser
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError(
                self.error_messages['invalid_email'],
                code='invalid_email',
            )
        return email

    def clean_security_answer(self):
        email = self.cleaned_data.get('email')
        security_answer = self.cleaned_data.get('security_answer')
        User = CustomUser
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return security_answer
        if user.security_question != security_answer:
            raise forms.ValidationError(
                self.error_messages['invalid_security_answer'],
                code='invalid_security_answer',
            )
        return security_answer
