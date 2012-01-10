from django.contrib.localflavor.us.forms import USPhoneNumberField
from django import forms

from one80.auth.models import UserProfile


class UserProfileForm(forms.ModelForm):
    phone = USPhoneNumberField(required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = UserProfile
        fields = ('phone', 'email')

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance'):
            if not kwargs.get('initial'):
                kwargs['initial'] = {}
            kwargs['initial'].update({'email': kwargs['instance'].email})
        super(UserProfileForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        self.instance.email = self.cleaned_data['email']

class UserProfileAdminForm(UserProfileForm):

    class Meta:
        model = UserProfile
        fields = ('user', 'phone', 'email')

