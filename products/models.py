from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=120)
    image=models.ImageField(upload_to='products', default="no_image.webp")
    price=models.FloatField(help_text="in USD")
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    added_by=models.ForeignKey(User, verbose_name="product_added_by", on_delete=models.CASCADE)
    def __str__(self):
        return  f'Product: {self.name}| Price {self.price}| Created on {self.created_on.strftime("%d/%m/%y") } '


    

