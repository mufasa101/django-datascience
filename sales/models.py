from django.db import models
from django.utils import timezone
from products.models import Product
from profiles.models import Profile
from customers.models import Customer
from .utils import generate_transaction_id
from django.shortcuts import reverse

# Create your models here.
class Position(models.Model):
    product=models.ForeignKey(Product, verbose_name="product_sales", on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    price=models.FloatField(blank=True,null=True)
    created_on=models.DateTimeField(blank=True,null=True)
    def save(self,*args,**kwargs):
        self.price=self.product.price *self.quantity
        return super().save(*args,**kwargs)
    def get_sales_id(self):
        sales_id=self.sale_set.first()
        # sales_ids=self.sale_set.all()
        # THIS IS FOR: perfomring a reverse relationship
        return sales_id.id
    def __str__(self):
        return  f'Product: {self.product.name} quantity: {self.quantity} price: {self.price} '
    
class Sale(models.Model):
    transaction_id=models.CharField(max_length=12,blank=True)
    positions=models.ManyToManyField(Position, verbose_name="position_sale")
    total_price=models.FloatField(blank=True,null=True)
    sales_guy=models.ForeignKey(Profile, verbose_name="sales_guy_profile", on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer, verbose_name="customer_customer", on_delete=models.CASCADE)
    updated_on=models.DateTimeField(auto_now=True)
    created_on=models.DateTimeField(blank=True,null=True)
    def save(self,*args,**kwargs):
        if self.transaction_id == "":
            self.transaction_id=generate_transaction_id()
        if self.created_on is None:
            self.created_on=timezone.now()
        return super().save(*args,**kwargs)
    def get_positions(self):
        return self.positions.all()
    def get_absolute_url(self):
        return reverse("sales:detail", kwargs={"pk": self.pk})

    def __str__(self):
        return  f'Sales: ({self.transaction_id}) {self.total_price}'
    
class CSV(models.Model):
    file_name = models.CharField(max_length=120, null=True)
    sales_file = models.FileField(upload_to='csv', null=True)
    activated=models.BooleanField(default=False)
    updated_on=models.DateTimeField(auto_now=True)
    created_on=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.file_name


