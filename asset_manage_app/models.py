from django.db import models
from django.utils import timezone

import datetime

# Create your models here.
class housekeep(models.Model):
    CATEGORY = (
        ("Grocery", "Grocery"),
        ("Restaurant", "Restaurant"),
        ("Internet", "Internet"),
        ("Fashion", "Fashion"),
        ("Study", "Study"),
        ("Medical", "Medical"),
        ("Subscription", "Subscription"),
        ("Utilities", "Utilities"),
        ("Other", "Other")
    )
    date = models.DateField(default = datetime.date.today)
    category = models.CharField(max_length=30, choices = CATEGORY, blank=True)
    description = models.TextField()
    amount = models.IntegerField()