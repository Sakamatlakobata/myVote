from django.contrib.auth.models import User
from django.db import models

# BILL_TYPES = [
#     ('H.R.',         'House Bill'),
#     ('S.',           'Senate Bill'),
#     ('H.J. Res.',    'House Joint Resolution'),
#     ('S.J. Res.',    'Senate Joint Resolution'),
#     ('H. Con. Res.', 'House Concurrent Resolution'),
#     ('S. Con. Res.', 'Senate Concurrent Resolution'),
#     ('H. Res.',      'House Simple Resolution'),
#     ('S. Res.',      'Senate Simple Resolution'),
# ]

VOTE_TYPES = [
    ('approve',    'Approve'),
    ('disapprove', 'Disapprove'),
    ('undecided',  'Undecided'),
    ('abstain',    'Abstain'),    
]

class Bill(models.Model):
    bill_id = models.CharField(max_length=16, null=True, blank=True)
    type    = models.CharField(max_length=8,  null=True, blank=True)
    # type    = models.CharField(max_length=16, choices=BILL_TYPES, default='H.R.')
    number  = models.CharField(max_length=16,  null=True, blank=True)
    text    = models.CharField(max_length=255, null=True, blank=True)
    url     = models.CharField(max_length=128, null=True, blank=True)
    date_introduced = models.DateField(null=True, blank=True) # date introduced

    def _get_full_name(self):
        return '{0} {1}'.format(str(self.number), self.text)
    full_name = property(_get_full_name)

    def __str__(self):
        return self.full_name


class Poll(models.Model):
    bill  = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name="polls", null=True, blank=True)
    vote  = models.CharField(max_length=64, choices=VOTE_TYPES, default='abstain')
    # count = models.IntegerField(default=0)
    user  = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '%s %s - %s - %s - %s' % (self.bill.type, self.bill.number, self.bill.text, self.user.username, self.vote)
        # return '%s %s - %s %s %i' % (self.bill.type, self.bill.number, self.bill.text, self.vote, self.count)
    
    class Meta:
        ordering = ['bill',]
