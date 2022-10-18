from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# import debug_toolbar


 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('product.urls')),
    path('',include('accounts.urls')),
    path('accounts/', include('accounts.passwords.urls')), 
    path('',include('wishlist.urls')),
    path('',include('search.urls')),
    path('',include('cart.urls')),
    path('',include('address.urls')),
    path('',include('orders.urls')),
    path('',include('review.urls')),
    path('',include('home.urls')),

    path('ckeditor/', include('ckeditor_uploader.urls')),
    # path('__debug__/', include(debug_toolbar.urls)),  
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)


admin.site.site_title = "Chroma"
admin.site.index_title = "Chroma"
admin.site.site_header = "Chroma"



