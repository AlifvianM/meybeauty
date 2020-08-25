from django import forms
from .models import Product, OrderItem, Order, Pembayaran, Member, Reseller
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
	class Meta:
		model = Pembayaran
		fields = '__all__'
            
            
class OrderUpdateForm(forms.ModelForm):
    alamat = forms.CharField(
            widget=forms.Textarea(
                    attrs = {
                        'class':'form__input form__input--2'
                    }
                ), required=True   
        )
    berat = forms.IntegerField(
            widget=forms.NumberInput(
                    attrs = {
                        'class':'form-control'
                    }
                )
        )

    class Meta:
        model = Order
        fields = (
        		'provinsi_tujuan',
				'kota_tujuan',
				'kecamatan_tujuan',
				'jasa_ongkir',
				'harga_ongkir',
                'alamat',
                # 'berat',
        	)


        
class OrderBayarForm(forms.ModelForm):
    bukti_pembayaran = forms.ImageField(
            widget= forms.FileInput(
                    attrs={
                        'class':'form__input form__input--2',
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
                        'class':'form__input form__input--2',
                    }
                )
        )
    email = forms.EmailField(
            widget=forms.EmailInput(
                    attrs={
                        'class':'form__input form__input--2',
                    }
                )
        )
    nomor_telepon = forms.CharField(
            widget=forms.NumberInput(
                    attrs={
                        'class':'form__input form__input--2',
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

class OrderResiForm(forms.ModelForm):
    resi = forms.CharField(
            widget=forms.TextInput(
                    attrs={
                        'class':'form__input form__input--2',
                    }
                )
        )
    class Meta:
        model = Order
        fields = (
            'resi',
            )
    
class ResellerForm(forms.ModelForm):
    nama = forms.CharField(
            widget=forms.TextInput(
                    attrs={
                        'class':'form__input form__input--2',
                    }
                )
        )
    email = forms.EmailField(
            widget=forms.EmailInput(
                    attrs={
                        'class':'form__input form__input--2',
                    }
                )
        )
    nomor_telepon = forms.CharField(
            widget=forms.NumberInput(
                    attrs={
                        'class':'form__input form__input--2',
                    }
                ), label='Nomor HP / Whatsapp'
        )
    alasan = forms.CharField(
            widget=forms.Textarea(
                    attrs={
                        'class':'form__input',
                    }
                )
        )
    terms = forms.BooleanField(
            widget=forms.CheckboxInput(
                    attrs={
                        'class':'form-control',
                    }
                )
        )
    class Meta:
        model = Reseller
        fields = (
            'nama',
            'email',
            'nomor_telepon',
            'alasan',
            'terms',
            )




