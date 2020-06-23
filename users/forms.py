from django import forms
from .models import Profile
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm


class UserRegisterForm(UserCreationForm):
	first_name = forms.CharField(
			widget=forms.TextInput(
					attrs = {
						'class':'form__input form__input--2',
						# 'id':'first_name'
						# 'name':'fir'
					}
				)
		)
	
	last_name = forms.CharField(
			widget=forms.TextInput(
					attrs={
						'class':'form__input form__input--2'
					}
				)
		)

	username = forms.CharField(
			widget=forms.TextInput(
					attrs={
						'class':'form__input form__input--2'
					}
				)
		)

	email = forms.EmailField(
    		widget=forms.EmailInput(
    				attrs = {
    					'class' : 'form__input form__input--2',
    					'type' : 'email'
    				}
    			), max_length=200, help_text='Required'
    	)

	password1 = forms.CharField(
			widget=forms.PasswordInput(
					attrs = {
						'class':'form__input form__input--2',
						'type' : 'password'
					}
				),
			label = 'Password'
		)

	password2 = forms.CharField(
			widget=forms.PasswordInput(
					attrs = {
						'class':'form__input form__input--2',
						'type' : 'password'
					}
				),
			label = 'Password Confirmation'
		)

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email']

class MyAuthForm(AuthenticationForm):
	username =forms.CharField(
			widget=forms.TextInput(
					attrs = {
						'class':'form__input form__input--2',
						
					}
				),
			label = 'Username'
		)

	password = forms.CharField(
    		widget=forms.PasswordInput(
    				attrs={
    					'class':'form__input form__input--2',
    					'type':'password'
    				}
    			)	
    	)

	error_messages = {
        'invalid_login': _(
            "Username atau Password anda salah. Mohon periksa kembali."
            # "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }




class MyLoginView(LoginView):
    authentication_form = MyAuthForm

class ProfileForm(forms.ModelForm):
	no_hp = forms.CharField(
			widget=forms.TextInput(
					attrs = {
						'class':'form__input form__input--2',
						'type':'number'
					}
				)
		)
	class Meta:
		model = Profile
		fields = (
        	'no_hp',
        	)
