from django.db import models

class Wpis(models.Model):
    tytul = models.CharField(max_length=1024)
    class Meta:
        app_label = '' #http://stackoverflow.com/questions/4382032