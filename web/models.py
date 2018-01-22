from django.db import models

# Create your models here.


class Jpider_response(models.Model):
    url = models.CharField(max_length=300)
    headers = models.CharField(max_length=1000)
    data = models.CharField(max_length=100)
    cookies = models.CharField(max_length=1000)


class Jpider_memory(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    extfield1 = models.CharField(max_length=300)
    extfield2 = models.CharField(max_length=300)
    extfield3 = models.CharField(max_length=300)
    extfield4 = models.CharField(max_length=300)
    extfield5 = models.CharField(max_length=300)
    extfield6 = models.CharField(max_length=300)
    extfield7 = models.CharField(max_length=300)
    extfield8 = models.CharField(max_length=300)
    extfield9 = models.CharField(max_length=300)
    extfield10 = models.CharField(max_length=300)