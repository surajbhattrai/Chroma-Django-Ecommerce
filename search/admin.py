from django.contrib import admin
from .models import SearchTerms 


# admin.site.register(SearchTerms)
 

@admin.register(SearchTerms)
class SearchTermsAdmin(admin.ModelAdmin):
    list_display = ['search_terms','total_searches']
    search_fields = ['search_terms']
    list_per_page = 100
    list_filter = ['updated_on']
    ordering = ('-total_searches',)


