from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User

class LoginForm(forms.Form):
    phone = forms.IntegerField(label='Your Phone Number')
    password = forms.CharField(widget=forms.PasswordInput)


class VerifyForm(forms.Form):
    key = forms.IntegerField(label='Please Enter OTP here')


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone',)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        qs = User.objects.filter(phone=phone)
        if qs.exists():
            raise forms.ValidationError("Phone number is taken")
        return phone

    def clean_password2(self):
        # Check if the two passwords match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2



class TempRegisterForm(forms.Form):
    phone = forms.IntegerField()
    otp = forms.IntegerField()


class SetPasswordForm(forms.Form):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)




class UserAdminCreationForm(forms.ModelForm):
    # Form for creating new users. It includes all the required fields and a repeated password
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone',)

    def clean_password2(self):
        # Check if the two passwords match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password 2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def save(self, commit=True):
        # save the password in a hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # user.active = False
        if commit:
            user.save()
        return user



class UserAdminChangeForm(forms.ModelForm):
    # Form for updating users. It includes all the fields.
    # It replaces the password feild with the admin password hash
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('phone', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, we will return the initial value
        # This is implemented here because the field does not have access to the initial value
        return self.initial["password"]