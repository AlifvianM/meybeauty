from django import forms
from shop.models import Order, Product, Member
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class OrderForm(forms.ModelForm):
	# status_order = forms.BooleanField(
	# 		widget=forms.CheckboxInput(
	# 				attrs = {
	# 					'class': 'form-check-input',
	# 				}
	# 			)
	# 	)
	resi = forms.CharField(
			widget=forms.TextInput(
					attrs = {
						'class':'form-control',
						'placeholder':'Masukkan Nomor Resi'
					}
				)
		)

	class Meta:
		model = Order
		fields = (
        	# 'status_order',
        	'status_bayar',
        	'resi',
        	)

class ProductForm(forms.ModelForm):
	nama = forms.CharField(
			widget=forms.TextInput(
					attrs = {
						'class':'form-control',
						'placeholder':'Masukkan Nama Product'
					}
				)
		)
	harga = forms.CharField(
			widget=forms.NumberInput(
					attrs = {
						'class':'form-control',
						'min':'1000',
						'placeholder':'Min : Rp.1000'
					}
				)
		)
	foto = forms.FileField(
			widget=forms.FileInput(
					attrs = {
						'class':' form-control ',
					}
				)
		)
	desc = forms.CharField(widget=SummernoteWidget())
	berat = forms.CharField(
			widget=forms.NumberInput(
					attrs = {
						'class':'form-control',
						'min':'1',
						'placeholder':'Min : 1 gr'
					}
				), label='Berat (gr)'
		)
	class Meta:
		model = Product
		fields = (
        	'nama',
        	'harga',
        	'foto',
        	'desc',
        	'berat',
        	)

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = (
        	'is_confirm',
        	)
    