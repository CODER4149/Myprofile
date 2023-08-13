from django.db import models

# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=20, blank=True, null=True)
    message = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Member(models.Model):
    Name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    message = models.CharField(max_length=255, default='0000000')

    def __str__(self):
        return f"{self.Name} {self.email}"


class Description(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=20, blank=True, null=True)
    message = models.CharField(max_length=20, blank=True, null=True)
    logo = models.ImageField(upload_to='item_images', blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    mobile_number = models.CharField(max_length=10, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Resume(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    resume_file = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class front_images(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(max_length=200, blank=True, null=True)
    logo = models.ImageField(upload_to='item_images', blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


#from django.db import models

class about(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    designation = models.CharField(max_length=100 , blank=True, null=True)
    mobile_number = models.CharField(max_length=10, blank=True, null=True)
    natinality = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"