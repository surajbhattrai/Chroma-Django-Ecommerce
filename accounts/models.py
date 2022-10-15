from django.urls import reverse
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import pre_save, post_save,post_delete
from helper import unique_code_generator 
import requests
from django.utils.safestring import mark_safe
from django.templatetags.static import static
from django.dispatch import receiver


 
 
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone, password, **extra_fields):
        """Create and save a User with the given phone and password."""
        if not phone:
            raise ValueError('The given phone must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        """Create and save a regular User with the given phone and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        """Create and save a SuperUser with the given phone and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)


class User(AbstractUser):
    username = None
    phone_regex = RegexValidator(regex=r'^\+?1?\d{1,10}$', message="Phone number must be entered in the format: '9876543210'. Up to 10 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=10, unique=True)
    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []
 

    def __str__(self):
        return str(self.phone)
        


class SMSActivation(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    code = models.CharField(max_length=7, unique=True)
    phone = models.CharField(null=True, max_length=20)
    activated = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    resend = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)

    def can_activate(self):
        qs = SMSActivation.objects.filter(pk=self.pk , activated=False)
        if qs.exists():
            return True
        return False

    def activate(self):
        if self.can_activate():
            user = self.user
            user.save()
            self.activated = True
            self.save()
            return True
        return False 

    def regenerate(self):
        self.code = unique_code_generator(self)
        self.resend += 1
        self.send_activation()
        return self.save()

    def send_reset(self):
        self.resend = 0
        return self.save()
    

    # def send_activation(self):
    #     pass

    def send_activation(self): 
        if self.resend < 10:
            if self.code:
                r = requests.post("http://api.sparrowsms.com/v2/sms",
                data={'token' : "v2_YDD09SrtAw3RMxNgWzASzerPIJs.JLEX",
                  'from'  : 'InfoSMS',
                  'to'    : self.phone,
                  'text'  : self.code + ' is your croma verification Code',})
                status_code = r.status_code
                response = r.text
                response_json = r.json()

                print(status_code)
                print(response)
                print(response_json)
        return False


def pre_save_sms_activation_receiver(sender, instance, *args, **kwargs):
    if not instance.activated:
        if not instance.code:
            instance.code = unique_code_generator(instance)

pre_save.connect(pre_save_sms_activation_receiver, sender=SMSActivation)


def post_save_user_create_receiver(sender, instance, created, *args, **kwargs):
    if created:
        obj = SMSActivation.objects.create(user=instance, phone=instance.phone)
        obj.send_activation()

post_save.connect(post_save_user_create_receiver, sender=User)




