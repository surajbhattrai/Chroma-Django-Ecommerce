from django import forms
from .models import Address
from django.forms import Select ,TextInput


 
class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ['building','area', 'city','district','province']
        widgets = {
            'building' :TextInput(attrs={'class': 'form-control form-control-sm','placeholder': 'Example : 2nd Floor , Computer Bazar.'}),
            'area' :TextInput(attrs={'class': 'form-control form-control-sm','placeholder': 'Example : Computer Bazar Area'}),
            'city' :TextInput(attrs={'class': 'form-control form-control-sm','placeholder': 'Example : Putalisadak'}),
            'district': Select(attrs={'class': 'form-control from-control-sm select2'}),
            'province' :Select(attrs={'class': 'form-control form-control-sm select2'}),
        }

    # def __init__(self, *args, **kwargs):
    #     super(AddressForm, self).__init__(*args, **kwargs)
    #     for visible in self.visible_fields():
    #         visible.field.widget.attrs['class'] = 'form-control form-control-sm'

  