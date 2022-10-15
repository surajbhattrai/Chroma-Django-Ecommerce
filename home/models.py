from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField


class Sliders(models.Model):
    image = models.ImageField(upload_to='seller/sliders')
    url = models.CharField(max_length=500 , blank=True)
      

 
class Pages(models.Model):
    name = models.CharField(max_length=100)
    content = RichTextField(blank=True)
    slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ("Page")
        verbose_name_plural = ("Pages")

    def get_absolute_url(self):
        return reverse("pages", kwargs={"slug":self.slug})




