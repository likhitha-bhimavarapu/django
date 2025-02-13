from django.db import models
from django.contrib.auth.models import User

from django.db import models
class Project(models.Model):
    CATEGORY_CHOICES = [
        ('ML', 'ML'),
        ('Python', 'Python'),
        ('Django', 'Django'),
        ('PHP', 'PHP'),
        ('Azure', 'Azure'),
        ('AWS', 'AWS'),          
        ('Flask', 'Flask'),      
        ('React', 'React'),      
    ]

    serial_number = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=200)
    project_pdf = models.FileField(upload_to='project_pdfs/')
    project_zip = models.FileField(upload_to='project_zips/')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.CharField(max_length=20, null=True, blank=True, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.project_name

class ProjectPurchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    purchased = models.BooleanField(default=False)
    order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15,null=True,blank=True)  # Added mobile number field
    message = models.TextField()


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.email}"