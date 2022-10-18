from django.contrib import admin
from .models import Product , Category , Variation 
from mptt.admin import DraggableMPTTAdmin




class VariationInline(admin.TabularInline):
    model = Variation
    extra = 1 

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','price','mrp','is_active','img','img_second']
    list_filter = ['published','updated']
    list_per_page = 100
    search_fields = ['title','description']
    list_editable=['is_active','img','img_second']
    inlines = [VariationInline] 


    # def render_change_form(self, request, context, *args, **kwargs):
    #     context['adminform'].form.fields['category'].queryset = Category.objects.filter(parent__isnull=True)
    #     return super(ProductAdmin, self).render_change_form(request, context, *args, **kwargs)


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation)



class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ['tree_actions','indented_title']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin) 
