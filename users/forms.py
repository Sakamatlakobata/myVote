from  django.contrib.auth.forms  import UserCreationForm, UserChangeForm, PasswordChangeForm
from  django.contrib.auth.models import User
from  django import forms
from .models import UserExtension


class UsersPasswordForm(PasswordChangeForm):
    old_password  = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model  = User
        fields = ('old_password', 'new_password1', 'new_password2')


# class UsersRegistrationForm(UserChangeForm):
#     username  = forms.CharField(widget = forms.TextInput(attrs    = {'class': 'form-control', 'placeholder': 'Please enter details'}))
#     first_name= forms.CharField(widget = forms.TextInput(attrs    = {'class': 'form-control'}))
#     last_name = forms.CharField(widget = forms.TextInput(attrs    = {'class': 'form-control'}))
#     email     = forms.EmailField(widget= forms.EmailInput(attrs   = {'class': 'form-control'}))
#     cell      = forms.CharField(widget = forms.TextInput(attrs    = {'class': 'form-control'}))
#     zipcode   = forms.CharField(widget = forms.TextInput(attrs    = {'class': 'form-control'}))
#     password1 = forms.CharField(widget = forms.PasswordInput(attrs= {'class': 'form-control'}))
#     password2 = forms.CharField(widget = forms.PasswordInput(attrs= {'class': 'form-control'}))

#     class Meta:
#         model  = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'cell', 'zipcode', 'password1', 'password2')

    #     widgets = {
    #         'username':  forms.TextInput(attrs={'class': 'form-control',}),
    #         # 'username':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Howzit'}),
    #         # 'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Howzit'}),
    #         'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Howzit'}),
    #         # 'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please enter details to register'}),
    #     }

    # # def __init__(self, *args, **kwargs):
    # #     super(RegistrationForm, self).__init__(*args, **kwargs)
    #     # self.fields['username'].widget.attrs['class']  = 'form-control'
    #     # self.fields['password1'].widget.attrs['class'] = 'form-control'
    #     # self.fields['password2'].widget.attrs['class'] = 'form-control'


# class UsersEditForm(UserCreationForm):
#     username    = forms.CharField(widget = forms.TextInput(attrs  = {'class': 'form-control', 'placeholder': 'Please enter details'}))
#     first_name  = forms.CharField(widget = forms.TextInput(attrs  = {'class': 'form-control'}))
#     last_name   = forms.CharField(widget = forms.TextInput(attrs  = {'class': 'form-control'}))
#     email       = forms.EmailField(widget= forms.EmailInput(attrs = {'class': 'form-control'}))
#     zipcode     = forms.CharField(widget = forms.TextInput(attrs = {'class': 'form-control'}))
#     last_login  = forms.CharField(widget = forms.DateInput(attrs  = {'class': 'form-control'}))
#     date_joined = forms.CharField(widget = forms.DateInput(attrs  = {'class': 'form-control'}))
#     password1   = forms.CharField(widget = forms.HiddenInput())
#     password2   = forms.CharField(widget = forms.HiddenInput())
#     # password1   = forms.CharField(widget = forms.PasswordInput(attrs= {'class': 'form-control', 'type': 'password'}))
#     # password2   = forms.CharField(widget = forms.PasswordInput(attrs= {'class': 'form-control', 'type': 'password', 'placeholder': 'Please confirm password'}))

#     class Meta:
#         model  = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'last_login', 'date_joined', 'password1', 'password2')


# class UsersProfileForm(forms.ModelForm):
#     model = UserExtension
#     fields = ['bio', 'website', 'facebook', 'twitter', 'image']
#     widgets = {
#         'bio':     forms.Textarea( attrs={'class': 'form-control'}),
#         'website': forms.TextInput(attrs={'class': 'form-control'}),
#         'facebook':forms.TextInput(attrs={'class': 'form-control'}),
#         'twitter': forms.TextInput(attrs={'class': 'form-control'}),
#         # 'image':   forms.TextInput(attrs={'class': 'form-control'}),
#     }


# class UsersRegistrationForm(UserCreationForm):
# 	email = forms.EmailField(required=True)

# 	class Meta:
# 		model  = User
# 		fields = ("username", "email", "password1", "password2")

# 	def save(self, commit=True):
# 		user = super(UsersRegistrationForm, self).save(commit=False)
# 		user.email = self.cleaned_data['email']
# 		if commit:
# 			user.save()
# 		return user


# class UsersExtensionRegistrationForm(UserCreationForm):
#     username=None
#     class Meta:
#         model  = UserExtension
#         fields = ("zipcode",)
