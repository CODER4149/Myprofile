from django.db import models

# Create your models here.
class Member(models.Model):
  Name = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  message = models.CharField(max_length=255,default='0000000')

  def __str__(self):
    return f"{self.Name} {self.email}"