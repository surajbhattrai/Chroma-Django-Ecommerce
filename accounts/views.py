from django.contrib.auth import login,authenticate ,update_session_auth_hash , logout
from django.utils.decorators import method_decorator
from django.shortcuts import redirect ,render,HttpResponseRedirect
from accounts.models import User, SMSActivation
from accounts.forms import SignUpForm, LoginForm, PasswordChangeCustomForm , UserUpdateForm
from django.views.generic import (View,ListView, CreateView, UpdateView, TemplateView)
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required


   
 
class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name= 'customer_signup.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            if request.user.is_authenticated:
                return redirect('home')
        except :
           pass
        return super().dispatch(request, *args, **kwargs)
  

    def form_valid(self, form):
        user = form.save()
        self.request.session['phone'] = user.phone
        return redirect('cverify')



def login_page(request):
    form = LoginForm(request.POST or None)
    valuenext= request.POST.get('next')
    if form.is_valid():
        phone = form.cleaned_data.get('phone')
        password = form.cleaned_data.get('password')
        user = authenticate(request, phone=phone, password=password)
        if user is not None:
            request.session['phone'] = user.phone
            try:
                obj = SMSActivation.objects.get(user=user, activated=True)
                login(request, user)
                if valuenext:
                    return HttpResponseRedirect(valuenext)
                return redirect('home')
                
            except SMSActivation.DoesNotExist :
                qs , qsCreated = SMSActivation.objects.get_or_create(user=user,phone=user.phone)
                qs.send_activation()
                messages.warning(request, "Verify Your Mobile Number.")
                return redirect('cverify')

    return render(request, 'customer_login.html',  {'form': form })



class CustomerInfo(ListView):
    model = User
    template_name = "customerinfo.html"



def user_logout(request):
    logout(request)
    return redirect('user_login')

 
@login_required(login_url='/login/')
def user_update(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your personal information has been updated!')
            return redirect('customerinfo')
    else: 
        form = UserUpdateForm(instance=request.user)
        context = {
            'form': form,
        } 
        return render(request, 'user_update.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeCustomForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('customerinfo')
    else:
        form = PasswordChangeCustomForm(request.user)
    return render(request, 'change_password.html', {'form': form })


def customer_verify(request):
    phone = request.session.get('phone')
    if request.method == "POST":
        code = request.POST["code"]
        try:
            qs = SMSActivation.objects.get(code=code, phone=phone)
            qs.activate()
            qs.send_reset()
            user = qs.user
            messages.success(request, 'Your phone number has been verified!')
            login(request, user)
            return redirect('home')
        except:
           messages.warning(request, "Invalid Verification Code")
           return redirect('cverify')
    else:
        phone = request.session.get('phone')
        context = {'phone': phone}
        return render(request, "verify.html",context)



def resend(request):
    url = request.META.get('HTTP_REFERER')
    phone = request.session.get('phone')
    try:
        obj = SMSActivation.objects.get(phone=phone)

        if obj.resend < 10 :
            obj.regenerate()
            obj.send_activation()
            messages.success(request, "Verification Code Send. Check Your Phone.")
        else:
            messages.warning(request, "Please contact customer care to activate your account.")
    except:
        pass
    return HttpResponseRedirect(url)




# def custom_password_reset(request):
#     if request.method == "POST":
#         mobile = request.POST['mobile']
#         try:
#             phone = SMSActivation.objects.get(phone=mobile)
#             phone.regenerate() 
#             request.session['phone'] = mobile
#             messages.success(request, 'Please verify your phone number.')
#             return redirect('reset_password_verify')
#         except:
#            messages.warning(request, "We cannot find an account with that mobile number.")
#            return redirect('custom_password_reset')
#     return render(request, 'registration/password_reset_form.html')


#Reset Password

def custom_password_reset(request):
    if request.method == "POST":
        mobile = request.POST['mobile']
        try:
            phone = SMSActivation.objects.get(phone=mobile)
            phone.regenerate() 
            request.session['phone'] = mobile
            messages.success(request, 'Please verify your phone number.')
            return redirect('reset_password_verify')
        except:
           messages.warning(request, "We cannot find an account with that mobile number.")
           return redirect('custom_password_reset')
    return render(request, 'registration/password_reset_form.html')




def reset_password_verify(request):
    phone = request.session.get('phone')
    if request.method == "POST":
        code = request.POST["code"]
        try:
            qs = SMSActivation.objects.get(code=code, phone=phone)
            qs.send_reset()
            user = qs.user
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            return redirect('password_reset_confirm', uidb64=uid ,token=token)
        except:
           messages.warning(request, "Invalid Verification Code")
           return redirect('reset_password_verify')
    else:
        phone = request.session.get('phone')
        context = {'phone': phone}
        return render(request, "verify.html",context)