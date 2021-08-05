from django.db import models

class Hash(models.Model):
    text = models.TextField()
    # SHA256 will be 64 char long
    hash = models.CharField(max_length=64)
