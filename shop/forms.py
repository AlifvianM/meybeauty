from django import forms
from .models import Product, OrderItem, Order, Pembayaran


class OrderItemForm(forms.ModelForm):
    quantity = forms.FloatField(
            widget=forms.NumberInput(
                    attrs = {
                        'class':'form-control',
                        'type':'number'

                    }
                ), initial='{{item.quantity}}'
        )

    class Meta:
        model = OrderItem
        fields = (
            'quantity',
            )
    


class PembayaranForm(forms.ModelForm):
	kode_nota = forms.ModelChoiceField(queryset=Order.objects.all(), 
            widget=forms.HiddenInput(
                    attrs = {
                        'class' : 'form-control',
                    }
                ), label='Jenis Cetak'   
        )

	# def __init__(self, *args, **kwargs):
 #        super().__init__(*args, **kwargs)
 #        self.fields['foo_select'].queryset = ...

	class Meta:
		model = Pembayaran
		fields = '__all__'
            
            
class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        # fields = '__all__'
        fields = (
        		'provinsi_tujuan',
				'kota_tujuan',
				'kecamatan_tujuan',
				'jasa_ongkir',
				'harga_ongkir',
        	)

class OrderBayarForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'bukti_pembayaran',
            )
        
    




