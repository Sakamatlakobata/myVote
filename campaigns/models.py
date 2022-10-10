from django.contrib.auth.models import User 
from district.utilities import get_district_number
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.db import models


class Campaign(models.Model):
    ''' Different types of contact '''
    name  = models.CharField(max_length=64, default="", null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, default="", null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_list')

    # def save(self, *args, **kwargs):
    #     self.owner = request.user
    #     super(Role, self).save(*args, **kwargs)


class Contact(models.Model):
    ''' Contact with voters  '''
    zipcode  = models.CharField(max_length=7,   null=True, blank=True)
    street   = models.CharField(max_length=64,  null=True, blank=True)
    number   = models.CharField(max_length=7,   null=True, blank=True)
    name     = models.CharField(max_length=64,  default="", null=True, blank=True)
    cell     = models.CharField(max_length=128, null=True, blank=True)
    email    = models.EmailField(max_length=64, default="", null=True, blank=True)
    date     = models.DateField(auto_now_add=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.SET_NULL, default="", null=True, blank=True, related_name='contact')
    owner    = models.ForeignKey(User, on_delete=models.SET_NULL, default="", null=True, blank=True, related_name='owner')
    district = models.IntegerField(default=0,   null=True, blank=True)
    notes    = RichTextField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.zipcode+', '+self.street+', '+self.number+', '+self.name+', '+self.cell+', '+self.email+', '+self.campaign.name+', '+str(self.date)

    # def get_absolute_url(self):
    #     return reverse('category_list')

    def save(self, *args, **kwargs):
        self.district = get_district_number(self.zipcode)
        super(Contact, self).save(*args, **kwargs)

