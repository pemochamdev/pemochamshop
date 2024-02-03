from django import forms

from orders.models import Payments, OrderProduct, Orders


class OrdersForm(forms.ModelForm):
    
    class Meta:
        model = Orders
        fields = (
            "first_name", 'last_name', 'email', 'phone', 
            'address_line_1', 'address_line_2', 'city', 
            'state', 'country', 'order_note'
        )
    


    def __init__(self, *args, **kwargs):
        super(OrdersForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['placeholder'] = 'First name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last name'
        self.fields['email'].widget.attrs['placeholder'] = 'email'
        self.fields['address_line_1'].widget.attrs['placeholder'] = 'Address Line 1'
        self.fields['address_line_2'].widget.attrs['placeholder'] = 'Address Line 2'
        self.fields['city'].widget.attrs['placeholder'] = 'City'
        self.fields['country'].widget.attrs['placeholder'] = 'Country'
        self.fields['state'].widget.attrs['placeholder'] = 'State'
        self.fields['order_note'].widget.attrs['placeholder'] = 'Order Note'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
