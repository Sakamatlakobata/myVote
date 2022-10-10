from django.contrib.auth.models import User 
from district.utilities import get_district_number
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.db import models


class Role(models.Model):
    ''' Role of member in the team '''
    name  = models.CharField(max_length=64, default="", null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, default="", null=True, blank=True, related_name='role')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_list')

    # def save(self, *args, **kwargs):
    #     self.owner = request.user
    #     super(Role, self).save(*args, **kwargs)


class UserExtension(models.Model):
    user     = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='userextension')
    office   = models.CharField(max_length=128, null=True, blank=True)
    cell     = models.CharField(max_length=128, null=True, blank=True)
    zipcode  = models.CharField(max_length=7,   null=True, blank=True)
    district = models.IntegerField(default=0,   null=True, blank=True)
    role     = models.ForeignKey(Role, on_delete=models.SET_NULL, default="", null=True, blank=True)

    bio      = RichTextField(blank=True, null=True)
    # bio      = models.TextField(blank=True)
    image    = models.ImageField(null=True, blank=True, upload_to="images/users")
    website  = models.URLField(max_length=128,  null=True, blank=True)
    facebook = models.CharField(max_length=128, null=True, blank=True)
    twitter  = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return str(self.user)

    def save(self): # override save account from form data to add the district number
        self.district = get_district_number(self.zipcode)
        super().save()

    # class Meta:
    #     ordering = ['user.last_name', 'user.first_name']


