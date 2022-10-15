from django.urls import path
from .views import order_processing , CustomerOrders , ajax_return_product, product_return , EsewaRequestView , EsewaVerifyView, KhaltiRequestView , KhaltiVerifyView

urlpatterns = [
    path('save_order/', order_processing, name="save_order"),
    path('customer/orders/', CustomerOrders.as_view(), name="customer_orders"),

    path('ajax_return_order/', ajax_return_product, name="return_order"),
    path('product_return/<int:id>', product_return, name="product_return"),

    path('esewarequest/',EsewaRequestView.as_view(),name='esewarequest'),
    path('esewa-verify/',EsewaVerifyView.as_view(),name='esewaverify'),

    path("khalti-request/", KhaltiRequestView.as_view(), name="khaltirequest"),
    path("khalti-verify/", KhaltiVerifyView.as_view(), name="khaltiverify"),

]   
