from django.db import models

# Create your models here.
class Depertment(models.Model):
    name = models.CharField(max_length=100)
    service = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name