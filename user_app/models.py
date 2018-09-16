from django.db import models

# Create your models here.
class User(models.Model):
    print('this is class User')
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=40)
    salt = models.CharField(max_length=20,null=True)
    status = models.BooleanField()
    note = models.CharField(max_length=50,null=True)
    class Meta:
        db_table = 't_user'