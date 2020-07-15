from django import forms
from .models import Product, OrderItem, Order, Pembayaran, Member
from .forms import OrderItem as OIModel


class OrderItemForm(forms.ModelForm):
    quantity = forms.FloatField(
            widget=forms.NumberInput(
                    attrs = {
                        'class':'form-control',
                        'type':'number'

                    }
                )
        )

    class Meta:
        model = OIModel
        fields = [
            'quantity',
            ]
    


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

# class OrderBayarForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = (
#             'bukti_pembayaran',
#             )
        
class OrderBayarForm(forms.ModelForm):
    bukti_pembayaran = forms.ImageField(
            widget= forms.FileInput(
                    attrs={
                        'class':'form-control',
                    }
                )
        )

    class Meta:
        model = Pembayaran
        fields = (
            # 'status_order',
            'bukti_pembayaran',
            )


class OrderItemForm2(forms.ModelForm):
        class Meta:
            model = OrderItem
            fields = (
                'order',
                )
            

class MemberForm(forms.ModelForm):
    nama = forms.CharField(
            widget=forms.TextInput(
                    attrs={
                        'class':'form-control',
                    }
                )
        )
    email = forms.EmailField(
            widget=forms.EmailInput(
                    attrs={
                        'class':'form-control',
                    }
                )
        )
    nomor_telepon = forms.CharField(
            widget=forms.NumberInput(
                    attrs={
                        'class':'form-control',
                    }
                ), label='Nomor HP / Whatsapp'
        )
    terms = forms.BooleanField(
            widget=forms.CheckboxInput(
                    attrs={
                        'class':'form-control',
                    }
                )
        )

    class Meta:
        model = Member
        fields = (
            'nama',
            'email',
            'nomor_telepon',
            'terms',
            )
    


