from django.db import models
from accounts.models import User

class SearchTerms(models.Model):
    search_terms = models.CharField(max_length=255, blank=True, null=True)
    total_searches = models.IntegerField(default=0)
    updated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Search Terms"

    def __str__(self):
        return self.search_terms 

 