from django.db import models

class account(models.Model):
    username = models.CharField(max_length = 30, null=True)
    auth_id = models.CharField(max_length = 40, null=True)

    def __unicode__(self):
        return self.username

class phone_number(models.Model):
    account = models.ForeignKey(account)
    number = models.CharField(max_length = 40, null=True)

    def __unicode__(self):
        return self.account.username
