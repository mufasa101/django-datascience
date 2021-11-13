from django.db import models
from profiles.models import Profile
from django.urls import reverse
# Create your models here.
class Report(models.Model):
    name=models.CharField(max_length=50)
    image=models.ImageField(upload_to="reports",blank=True)
    remarks=models.TextField(null=True,blank=True)
    created_by=models.ForeignKey(Profile, verbose_name="created_by_profile", on_delete=models.CASCADE)
    updated_on=models.DateTimeField(auto_now=True)
    created_on=models.DateField(auto_now_add=True)
    def get_absolute_url(self):
        return reverse("reports:detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.name
    class Meta:
        ordering=('-created_on',)
       
    