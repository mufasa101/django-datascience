from django.db import models

# Create your models here.
class Customer(models.Model):
    name=models.CharField(max_length=65)
    image=models.ImageField(upload_to='customers', default="no_image.webp")
    

    def __str__(self):
        return f'Customer: {self.name}'
