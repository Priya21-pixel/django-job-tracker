from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    
    link = models.URLField()
    date_applied = models.DateField()
    deadline = models.DateField()
    status = models.CharField(max_length=50, choices=[
        ('Applied', 'Applied'),
        ('Interview', 'Interview'),
        ('Offer', 'Offer'),
        ('Rejected', 'Rejected'),
        ('Shortlisted', 'Shortlisted'),
        ('Assessment', 'Assessment'),
        ('Hired', 'Hired'),

    ])

    def __str__(self):
        return f"{self.company} - {self.position}"
