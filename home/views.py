from django.shortcuts import render
from django.views.generic import ListView , DetailView
from product.models import Product
from .models import Pages , Sliders

class Home(ListView):
    template_name = "home.html"
    model = Product

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['products'] = Product.active.all()
        context['sliders'] = Sliders.objects.all()
        return context 


class PageDetail(DetailView):
    model = Pages
    template_name = "page.html"

