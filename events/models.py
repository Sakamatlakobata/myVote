# from django.urls import reverse
from django.contrib.auth.models import User
from district.utilities import get_district_number
from django.db import models

# rolls = [('venue', 'Venue Coordinator'), ('event', 'Event Planner')]
class Venue(models.Model):
    name     = models.CharField(max_length=128, null=True, blank=True)
    contact  = models.ForeignKey(User, related_name='events', on_delete=models.CASCADE)
    location = models.TextField(default='',   null=True, blank=True)
    zipcode  = models.CharField(max_length=7, null=True, blank=True)
    district = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.name
        # return self.name + ', ' + self.contact.first_name  + ' ' + self.contact.last_name  + ', ' + self.contact.email

    def save(self): # override save account from form data to add the district number
        self.district = get_district_number(self.zipcode)
        super().save()

    # def get_absolute_url(self):
    #     # return reverse('venue_list')
    #     return reverse('venue_update', kwargs={'pk': self.pk})


class Event(models.Model):
    name      = models.CharField(max_length=128, null=True, blank=True)
    contact   = models.ForeignKey(User,  related_name='event',  on_delete=models.CASCADE)
    venue     = models.ForeignKey(Venue, related_name='events', on_delete=models.CASCADE)
    attendees = models.ManyToManyField(User, related_name='attendees', blank=True)
    date      = models.DateField(null=True, blank=True)
    time      = models.TimeField(null=True, blank=True)
    # roll = models.CharField(choices=rolls, max_length=128, null=True, blank=True)

    def __str__(self):
        return self.name
        return self.name + ', ' + self.venue.name + ', ' + self.contact.first_name  + ' ' + self.contact.last_name  + ', ' + self.contact.email
