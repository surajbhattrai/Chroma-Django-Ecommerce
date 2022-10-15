from django.shortcuts import render ,get_object_or_404 ,redirect
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank , TrigramSimilarity
from django.db.models import Q ,Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Product , Category
from search.models import SearchTerms
from datetime import datetime, timedelta
from review.models import Review 
from wishlist.models import WishlistItem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from orders.models import OrderItem

   

class ProductDetail(DetailView):
    model = Product
    template_name = "product.html"
    paginate_by = 20


    def get_context_data(self, **kwargs): 
        slug = self.kwargs.get('slug')        
        product=Product.objects.get(slug=slug)
        object_list = Review.objects.prefetch_related('reply').filter(order_item__product=product, parent__isnull=True)
        context = super().get_context_data(object_list=object_list,**kwargs)
        if self.request.user.is_authenticated: 
            context["saved"] = WishlistItem.objects.select_related('wishlist').filter(wishlist__user=self.request.user ,product=product)

        return context


class CategoryView(ListView): 
    model = Product
    template_name = "category.html"

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)

        category = Category.objects.filter(parent=None)
        products = Product.active.all()

        #GET request ---> query
        query = self.request.GET.get('q')
        search_vectors = (
            SearchVector('title', weight='A') +
            SearchVector('description', weight='B')
            )
        search_query = SearchQuery(query)
        search_rank = SearchRank(search_vectors, search_query)
        trigram_similarity = TrigramSimilarity('title', query)

        if query:
            self.update_search_query(query) 
            products= products.annotate(search=search_vectors).filter(Q(search=search_query)).annotate(rank=search_rank + trigram_similarity)
 
        # GET request ---> Catgeory
        request_category = self.request.GET.get('category', None)
        sub_category = []
        if request_category:
            sub_category= Category.objects.get(slug=request_category).get_children()
            products = products.filter(category__slug=request_category)

        # GET request ---> Sub Catgeory
        request_sub_category = self.request.GET.get('subcategory', None)
        sub_subcategory = []
        if request_sub_category:
            products = products.filter(sub_category__slug=request_sub_category)
  
        paginator = Paginator(products, 40)            
        page = self.request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
    

        context = {
                'sub_category':sub_category,
                'products': products,
                'category': category,
                } 
        return context


    def update_search_query(self, query):
        term, _ = SearchTerms.objects.get_or_create(
            defaults={'search_terms':query}, 
            search_terms__iexact=query
        )
        term.total_searches += 1
        term.save()  





 





