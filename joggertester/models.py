from django.db import models

class Wpis(models.Model):
    subject = models.CharField(max_length=1024)
    content_short = models.CharField(max_length=10240)
    entry_id = models.CharField(max_length=32)
    date_day = models.CharField(max_length=32)
    date_month = models.CharField(max_length=32)
    date_year = models.CharField(max_length=32)
    comments_blocked = models.BooleanField()
    class Meta:
        app_label = '' #http://stackoverflow.com/questions/4382032

class Komentarz(models.Model):
    content = models.CharField(max_length=10240)
    entry_id = models.ForeignKey('Wpis.entry_id')
    class Meta:
        app_label = '' #http://stackoverflow.com/questions/4382032
