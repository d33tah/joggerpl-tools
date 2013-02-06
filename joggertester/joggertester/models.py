from django.db import models

class Wpis(models.Model):
    subject = models.CharField(max_length=1024)
    content_short = models.CharField(max_length=10240)
    entry_id = models.CharField(max_length=32)
    date_day = models.CharField(max_length=32)
    date_month = models.CharField(max_length=32)
    date_year = models.CharField(max_length=32)
    comments_blocked = models.BooleanField()

class Komentarz(models.Model):
    content = models.CharField(max_length=10240)
    wpis_id = models.ForeignKey('Wpis')
