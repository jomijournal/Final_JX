from __future__ import unicode_literals

from django.db import models

class det_ax(models.Model):
    si = models.CharField(max_length=128, unique=True)
    ip = models.CharField(max_length=128)
    org = models.CharField(max_length=128)
    time = models.CharField(max_length=128)
    timep = models.CharField(max_length=128)
    geol = models.CharField(max_length=128)
    month = models.CharField(max_length=128)
    year = models.CharField(max_length=128)
    ip_float = models.FloatField(default=0)

    def __str__(self):              # __unicode__ on Python 2
        return self.org
        
class cli_ax(models.Model):
    org = models.CharField(max_length=128, unique=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.org
