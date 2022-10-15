from django.db import models
from accounts.models import User
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver


DISTRICTS= (
    ('Achham','Achham'),
    ('Arghakhanchi','Arghakhanchi'),
    ('Baglung','Baglung'),
    ('Baitadi','Baitadi'),
    ('Bajhang','Bajhang'),
    ('Bajura','Bajura'),
    ('Banke','Banke'),
    ('Bara','Bara'),
    ('Bardiya','Bardiya'),
    ('Bhaktapur','Bhaktapur'),
    ('Bhojpur','Bhojpur'),
    ('Chitwan','Chitwan'),
    ('Dadeldhura','Dadeldhura'),
    ('Dailekh','Dailekh'),
    ('Dang deukhuri','Dang deukhuri'),
    ('Darchula','Darchula'),
    ('Dhading','Dhading'),
    ('Dhankuta','Dhankuta'),
    ('Dhanusa','Dhanusa'),
    ('Dholkha','Dholkha'),
    ('Dolpa','Dolpa'),
    ('Doti','Doti'),
    ('Gorkha','Gorkha'),
    ('Gulmi', 'Gulmi'),
    ('Humla','Humla'),
    ('Ilam', 'Ilam'),
    ('Jajarkot','Jajarkot'),
    ('Jhapa','Jhapa'),
    ('Jumla','Jumla'),
    ('Kailali','Kailali'),
    ('Kalikot','Kalikot'),
    ('Kanchanpur','Kanchanpur'),
    ('Kapilvastu','Kapilvastu'),
    ('Kaski','Kaski'),
    ('Kathmandu','Kathmandu'),
    ('Kavrepalanchok','Kavrepalanchok'),
    ('Khotang','Khotang'),
    ('Lalitpur','Lalitpur'),
    ('Lamjung','Lamjung'),
    ('Mahottari','Mahottari'),
    ('Makwanpur','Makwanpur'),
    ('Manang','Manang'),
    ('Morang','Morang'),
    ('Mugu','Mugu'),
    ('Mustang','Mustang'),
    ('Myagdi','Myagdi'),
    ('Nawalparasi','Nawalparasi'),
    ('Nuwakot','Nuwakot'),
    ('Okhaldhunga','Okhaldhunga'),
    ('Palpa','Palpa'),
    ('Panchthar','Panchthar'),
    ('Parbat','Parbat'),
    ('Parsa', 'Parsa'),
    ('Pyuthan','Pyuthan'),
    ('Ramechhap','Ramechhap'),
    ('Rasuwa','Rasuwa'),
    ('Rautahat','Rautahat'),
    ('Rolpa', 'Rolpa'),
    ('Rukum','Rukum'),
    ('Rupandehi','Rupandehi'),
    ('Salyan', 'Salyan'),
    ('Sankhuwasabha','Sankhuwasabha'),
    ('Saptari', 'Saptari'),
    ('Sarlahi','Sarlahi'),
    ('Sindhuli', 'Sindhuli'),
    ('Sindhupalchok','Sindhupalchok'),
    ('Siraha','Siraha'),
    ('Solukhumbu','Solukhumbu'),
    ('Sunsari','Sunsari'),
    ('Surkhet','Surkhet'),
    ('Syangja','Syangja'),
    ('Tanahu','Tanahu'),
    ('Taplejung','Taplejung'),
    ('Terhathum','Terhathum'),
    ('Udayapur','Udayapur')
)

PROVINCE= (
    ('one','Province No. 1'),
    ('two', 'Province No. 2'),
    ('three', 'Bagmati Province'),
    ('four', 'Gandaki Province'),
    ('five', 'Lumbini Province'),
    ('six', 'Karnali Province'),
    ('seven', 'Sudurpashchim Province'),
)

  
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    building = models.CharField(max_length=120,blank=True,null=True)
    area = models.CharField(verbose_name="Area",max_length=100, null=True, blank=True)
    city = models.CharField(verbose_name="City/Town",max_length=50)
    district = models.CharField(choices=DISTRICTS,verbose_name="District",max_length=100, default="Kathmandu")
    province = models.CharField(choices=PROVINCE,verbose_name="Province",max_length=100, default="three")
    default = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta: 
        ordering = ('-created',)
        
    def __str__(self):
        return str(self.user)

    def __str__(self):
        return 'Address of {} with id {}'.format(self.user, self.id)

    def current_address(self):
        return Address.objects.get(user=self.request.user, default=True)

    # def set_default(self):
    #     qs = Address.objects.exclude(id=self.id)
    #     qs.update(default=False)
    #     self.default = True
    #     self.save()
 

def address_post_save_receiver(sender, instance, created, *args, **kwargs):
    if instance.default:
        user = instance.user
        qs = Address.objects.filter(user=user).exclude(id=instance.id)
        qs.update(default=False)
        user.cart_user.update_total()

post_save.connect(address_post_save_receiver, sender=Address)

