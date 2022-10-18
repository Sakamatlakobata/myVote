from district.utilities import get_district_number
from django.contrib.auth.models import User 
from django.db import models


class Messaging(models.Model):
    subject  = models.CharField(max_length=128, null=True, blank=True)
    date     = models.DateField(auto_now_add=True)
    owner    = models.ForeignKey(User, on_delete=models.SET_NULL, default="", null=True, blank=True, related_name='messaging')
    district = models.IntegerField(default=0,  null=True, blank=True)
    zipcode  = models.CharField(max_length=7,  null=True, blank=True)
    street   = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        ordering = ['subject']

    def __str__(self):
        return self.subject+', '+str(self.date)+', '+str(self.district)+', '+self.zipcode+', '+self.street+', '+str(self.owner)

    def save(self, *args, **kwargs):
        self.district = get_district_number(self.zipcode)
        super(Messaging, self).save(*args, **kwargs)

