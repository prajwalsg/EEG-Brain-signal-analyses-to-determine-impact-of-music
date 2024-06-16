# in models.py
from django.db import models

class EEGData(models.Model):
    timestamp = models.DateTimeField()
    delta_tp9 = models.FloatField()
    delta_af7 = models.FloatField()
