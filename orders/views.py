from django.shortcuts import render, get_object_or_404,HttpResponseRedirect,redirect
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank , TrigramSimilarity
from django.db.models import Q
from django.contrib import messages
from django.db.models import Prefetch
from .models import Order , OrderItem, ReturnOrder
from product.models import Product
from cart.models import Cart , CartItem
from address.models import Address
from accounts.models import User
from django.views.generic import ListView , View
from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
import requests as req

 
 
@login_required(login_url='/login/')
def order_processing(request):
    if request.POST.get('address'): 
        cart = Cart.objects.get(user=request.user)
        order = Order.objects.create(user=request.user ,total=cart.total, coupon=cart.coupon , delivery_charge=cart.delivery_charge())
        order.save()
        for item in cart.items.all():
            orderItem, created = OrderItem.objects.update_or_create(
                order=order, product=item.product, price=item.price, quantity=item.quantity ,total=item.total ,color=item.color, size=item.size)
            order.order_items.add(orderItem)
        address = request.POST['address']
        order.address = Address.objects.get(id=address)
        order.instruction = request.POST['instruction']
        order.contact_number = request.POST['contact_number']
        order.payment_method = request.POST['payment_method']
        order.save()

        if request.POST['payment_method'] == "Esewa":
                return redirect(reverse("esewarequest") + "?o_id=" + str(order.id))
        elif request.POST['payment_method'] == "Khalti":                             
                return redirect(reverse("khaltirequest") + "?o_id=" + str(order.id))
        else:
            order.payment_completed = True
            order.save()
            cart.delete() 
            return redirect('order_success') 
    else:
        messages.warning(request, 'Please add an address before continuing')
        return redirect('cart')




class KhaltiRequestView(View):
    def get(self, request, *args, **kwargs):
        o_id = request.GET.get("o_id")
        order = Order.objects.get(id=o_id)
        context = {
            "order": order
        }
        return render(request, "khaltirequest.html", context)


class KhaltiVerifyView(View):
    def get(self, request, *args, **kwargs):
        token = request.GET.get("token")                    
        amount = request.GET.get("amount")                  
        o_id = request.GET.get("order_id")                  
        url = "https://khalti.com/api/v2/payment/verify/"   
        payload = {                                 
            "token": token,
            "amount": amount
        }
        headers = {                                
            "Authorization": "test_secret_key_"
        }
        order_obj = Order.objects.get(id=o_id)
        response = requests.post(url, payload, headers=headers)         
        resp_dict = response.json()               
        if resp_dict.get("idx"):                 
            success = True                        
            order_obj.payment_completed = True    
            order_obj.save()    
            cart = Cart.objects.get(user=request.user)
            cart.delete()                  
        else:                                     
            success = False                         
        data = {
            "success": success
        }
        return JsonResponse(data) 

            


class EsewaRequestView(View):
    def get(self,request,*args,**kwargs):
        o_id=request.GET.get('o_id')
        order= Order.objects.get(id=o_id)
        context={
             "order":order
        }
        return render(request,'esewarequest.html',context)


class EsewaVerifyView(View):
    def get(self,request,*args,**kwargs):
        import xml.etree.ElementTree as ET
        oid=request.GET.get('oid')
        amt=request.GET.get('amt')
        refId=request.GET.get('refId')
        url ="https://uat.esewa.com.np/epay/transrec"
        d = {
            'amt': amt,
            'scd': 'epay_payment',
            'rid':refId ,
            'pid':oid,
        }
        resp = req.post(url, d)
        root = ET.fromstring(resp.content)
        status=root[0].text.strip()
        order_id=oid.split("_")[1]
        order_obj=Order.objects.get(id=order_id)
        if status == "Success":
            order_obj.payment_completed = True
            order_obj.save()
            cart = Cart.objects.get(user=request.user)
            cart.delete()
            return redirect('order_success')
        else:
            order_obj.delete()
            messages.warning(request, 'Payment failed. Please try again.')
            return redirect('cart')


 

class CustomerOrders(LoginRequiredMixin,ListView):
    model = Order
    template_name = "customer_orders.html"
    login_url = '/customer/login/' 
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(CustomerOrders, self).get_queryset(*args, **kwargs)
        qs = qs.prefetch_related("order_items__product").filter(user = self.request.user,payment_completed= True).order_by('-created')
        return qs 



def ajax_return_product(request):
    order_item_id = request.GET.get('id', None)
    item = OrderItem.objects.get(id=order_item_id)
    return render(request, 'return_form.html', {'item': item})


@login_required(login_url='/login/')
def product_return(request ,id):
    url = request.META.get('HTTP_REFERER')
    order_item = OrderItem.objects.get(id=id)
    reason = request.POST['reason']
    return_request = ReturnOrder.objects.update_or_create(user=request.user, reason=reason, order_item=order_item)    
    messages.success(request, 'Your product return request has been successfully sent.')
    return HttpResponseRedirect(url)


    
        