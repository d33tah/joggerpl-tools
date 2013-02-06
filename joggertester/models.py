from django.db import models

class Wpis(models.Model):
    subject = models.CharField(max_length=1024)
    entry_id = models.CharField(max_length=32)
    class Meta:
        app_label = '' #http://stackoverflow.com/questions/4382032