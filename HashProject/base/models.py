from django.db import models


# Create your models here.


class UserProfile(models.Model):
    email = models.EmailField(max_length=254, null=False)
    jwtToken = models.CharField(max_length=200)
    avatar = models.ImageField(null=True, default="avatar1.svg")
    updated = models.DateTimeField(auto_now=True)
    

    ispc = models.BooleanField(null=True)
    ismobile = models.BooleanField(null=True)
    istablet = models.BooleanField(null=True)
    istouchcapable = models.BooleanField(null=True)
    isbot = models.BooleanField(null=True)
    browserfamily = models.CharField(max_length=255, null=True)
    browserversion = models.CharField(max_length=255, null=True)
    browserversionstring = models.CharField(max_length=255, null=True)
    os = models.CharField(max_length=255, null=True)
    osversion = models.CharField(max_length=255, null=True)
    devicefamily = models.CharField(max_length=255, null=True)
    http_xforwarded_for = models.TextField(max_length=255, null=True)
    ipaddress = models.CharField(max_length=255, null=True)
    useragent = models.TextField(null=True)


    def __str__(self):
        return self.email

