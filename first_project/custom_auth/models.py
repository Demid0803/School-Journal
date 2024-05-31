from django.db import models
import hashlib
from datetime import datetime


# Create your models here.
class PseudoUser(models.Model):
    email = models.CharField(max_length=50, primary_key=True)
    password_hash = models.CharField(max_length=64)
    role = models.CharField(max_length=10)
    role_id = models.PositiveIntegerField()

    def save(self, **kwargs):
        self.password_hash = hashlib.sha256(self.password_hash.encode()).hexdigest()
        super().save(**kwargs)


class Token(models.Model):
    email = models.CharField(max_length=50, primary_key=True)
    date_expired = models.DateTimeField()
    token = models.CharField(max_length=128)