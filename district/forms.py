from  django.contrib.auth.forms  import UserCreationForm
from  django.contrib.auth.models import User
from  django.db import models
from  django    import forms
# from .models    import Account
from .utilities import get_district_number


class GetZIPcode(forms.Form):
    ZIPcode = forms.CharField(max_length=5, label="ZIP code")
    # ZIPcode = forms.IntegerField(label="ZIP code")
    # ZIPcode = forms.IntegerField(min_value='00001', label="ZIP code") # '<' not supported between instances of 'int' and 'str'
    # ZIPcode = forms.IntegerField(min_value='00001', max_value='99999', label="ZIP code") # '<' not supported between instances of 'int' and 'str'


class UserForm(UserCreationForm):
    class Meta:
        model  = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2',]


# class AccountsForm(forms.ModelForm):
#     class Meta:
#         model  = Account
#         fields = ['zipcode',]
#         # fields = ['zipcode', 'district_number',]


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    zipcode = models.CharField(max_length=5)
    # district = models.CharField(max_length=50, blank=True, null=True)
    district_number = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.user.username

    def save(self): # override save account from form data to add the district number
        self.district_number = get_district_number(self.zipcode)
        super().save()
