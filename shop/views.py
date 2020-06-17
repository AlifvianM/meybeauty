from django.shortcuts import render, redirect
from .models import Product, OrderItem, Order, Pembayaran
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from datetime import datetime
from users.models import Profile
from django.conf import settings
from django.db.models import Avg, Sum, Count
from .forms import PembayaranForm, OrderUpdateForm,OrderBayarForm, OrderItemForm
from rajaongkir import RajaOngkirApi

from django.views.generic.edit import CreateView, UpdateView, DeleteView

import http.client
import requests
import datetime
import json

# Create your views here.


def cek_ongkir(request,kota_id, kecamatan_tujuan_id, berat, jasa_ongkir):
	kota_id = kota_id
	kecamatan_tujuan_id = kecamatan_tujuan_id
	berat = berat
	jasa_ongkir = jasa_ongkir
	conn = http.client.HTTPConnection("pro.rajaongkir.com")
	url = "https://pro.rajaongkir.com/api/cost"  #origin=501&originType=city&destination=574&destinationType=subdistrict&weight=1700&courier=jne
	print(url)
	payload = "origin=" + kota_id + "&originType=city&destination=" + kecamatan_tujuan_id + "&destinationType=subdistrict&weight=" + str(berat) + "&courier=" + jasa_ongkir
	
	r = requests.post(url,payload, headers = { 'key': settings.API_KEY_SECRET, 'content-type': "application/x-www-form-urlencoded" })
	# r = conn.request("POST","/api/cost",payload, headers = { 'key': settings.API_KEY_SECRET, 'content-type': "application/x-www-form-urlencoded" })
	
	ongkir = r.json()

	# for o in ongkir.values():
	# 	print(o['results'])
	print(json.dumps(ongkir, indent=2))

	context = {
		'ongkir':ongkir,
		'kota_asal':kota_id,
		'kecamatan_tujuan':kecamatan_tujuan_id,

	}

	return render(request, 'shop/ongkir.html', context)




def cek_kecamatan_tujuan(request, kota_tujuan_id):
	kota_tujuan_id = kota_tujuan_id
	url = "https://pro.rajaongkir.com/api/subdistrict?city=" + str(kota_tujuan_id)
	# print(url)
	r = requests.get(url, headers = { 'key': settings.API_KEY_SECRET })
	kecamatan = r.json()
	context = {
		'kecamatan':kecamatan,
	}
	return render(request, 'shop/kecamatan.html', context)





def cek_kota_tujuan(request, prov_tujuan_id):
	prov_tujuan_id = prov_tujuan_id
	url = "https://pro.rajaongkir.com/api/city?province=" + prov_tujuan_id
	# print(url)
	headers = { 'key': settings.API_KEY_SECRET }
	r = requests.get(url, headers)
	kota = r.json()

	print(json.dumps(kota, indent=2))

	context = {
		'city':kota,

	}
	return render(request, 'shop/kota_tujuan.html', context)

def cek_kota(request, prov_id):
	prov_id = prov_id
	url = "https://pro.rajaongkir.com/api/city?province=" + prov_id
	print(url)
	headers = { 'key': settings.API_KEY_SECRET }
	r = requests.get(url, headers)
	kota = r.json()
	# print(json.dumps(kota, indent=3))
	context = {
		'city':kota,
		'prov_id': prov_id
	}
	return render(request, 'shop/kab.html', context)


def cek_provinsi(request):
	url = "https://pro.rajaongkir.com/api/province"
	headers = { 'key': settings.API_KEY_SECRET }
	r = requests.get(url, headers)
	
	provinces = r.json()
	# print(json.dumps(provinces, indent=3))

	context = {
		'provinces':provinces,
		# 'city':list_of_city,
	}
	template = 'shop/checkout_page.html'
	return render(request, template, context)


def product_list(request):
	pl = Product.objects.all()
	items = OrderItem.objects.filter(order__user = request.user, order__status_order = False)
	total = OrderItem.objects.filter(order__status_order = False).aggregate(Sum('price'))['price__sum'] or 0.00
	count_items = OrderItem.objects.filter(order__status_order = False).aggregate(Count('id'))['id__count'] or 0.00
	form = OrderItemForm(request.POST or None)

	if form.is_valid():
		form.save()
		return redirect(reverse('shop-checkout', kwargs = {'id':self.items.order.id}))

	context = {
		'products' : pl,
		'items':items,
		'subtotal':total,
		'count_items':count_items,
		'form':form,
	}
	template = 'shop/home.html'
	return render(request, template, context)

def product_detail(request, slug):
	obj = get_object_or_404(Product, slug=slug)
	context = {
		'obj':obj
	}
	template = 'shop/product-details.html'
	return render(request, template, context)


# def add_to_cart(request, **kwargs):
#     # get the user profile
#     # user_profile = get_object_or_404(Profile, user=request.user)
#     # filter products by id
#     product = Product.objects.filter(slug=kwargs.get('slug')).first()
#     # check if the user already owns this product
#     # if product in request.user.profile.ebooks.all():
#     #     messages.info(request, 'You already own this ebook')
#     #     return redirect(reverse('products:product-list')) 
#     # create orderItem of the selected product
#     order_item, status = OrderItem.objects.get_or_create(product=product)
#     # create order associated with the user
#     user_order, status = Order.objects.get_or_create(
#     	# owner=user_profile, 
#     	is_ordered=False)
#     print(user_order, status)
#     user_order.items.add(order_item)
#     # user_order.created.add(datetime.now)
#     if status:
#         # generate a reference code
#         # user_order.ref_code = generate_order_id()
#         user_order.save()

#     # show confirmation message and redirect back to the same page
#     messages.info(request, "item added to cart")
#     return redirect(reverse('shop-detail', kwargs={'slug':order_item.product.slug}))


# def add_to_cart(request, **kwargs):
#     # user_profile = get_object_or_404(Profile, user = request.user)
#     product = Product.objects.filter(slug = kwargs['slug']).first()
#     order_item = OrderItem.objects.get_or_create(product=product)
#     print(order_item)
#     user_order = Order.objects.get_or_create(owner=request.user, is_ordered=False)
#     print(user_order)
#     # for u in user_order:
#     #     u.items.add(order_item)
#     #     u.save()
#     print(user_order)
#     user_order.save()
#     return redirect(reverse('shop-list'))



def add_to_cart(request,pk):
    product = get_object_or_404(Product, pk=pk)
    cart,created = Order.objects.get_or_create(
        user=request.user,
         status_order = False,
         )
    cart.kode_nota = str(datetime.datetime.now())
    print('cart :', cart, 'kode nota', cart.kode_nota)
    print('created :', created)
    orderitem,created = OrderItem.objects.get_or_create(product=product,order=cart, price=product.harga)
    total = OrderItem.objects.filter(order__status_order = False).aggregate(Sum('price'))['price__sum'] or 0.00
    # order.quantity += 1
    if created:
	    orderitem.order.kode_nota = str(datetime.datetime.now())
	    orderitem.order.harga = total
	    orderitem.save()
	    print(orderitem)
	    cart.save()
    messages.success(request, "Cart updated!")
    return redirect('shop-list')


# 2020-06-06 05:24:29.900785


def delete_from_cart(request, **kwargs):
    item_to_delete = OrderItem.objects.filter(product__slug=kwargs['slug'])
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect('shop-list')

def show_cart(request):
	items = OrderItem.objects.filter(order__user = request.user, order__status_order = False)
	all_items = OrderItem.objects.filter(order__user = request.user)
	total = OrderItem.objects.filter(order__status_order = False).aggregate(Sum('price'))['price__sum'] or 0.00

	context = {
		'items':items,
		'item_true':all_items,
		'total':total,
	}
	return render(request, 'shop/cart.html', context)

class OrderItemDeleteView(DeleteView):
    model = OrderItem
    # template_name = "shop/delete.html"


    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('shop-list')

# def pembayarancreate(request, kode_nota):
# 	kode_nota = get_object_or_404(Order, kode_nota=kode_nota)
# 	kode_nota = kode_nota
# 	# pembayaran, created = Pembayaran.objects.get_or_create(kode_nota = kode_nota)
# 	# print(pembayaran.kode_nota)

# 	# pembayaran.kode_nota = kode_nota
# 	# pembayaran.save()
# 	forms = PembayaranForm(request.POST or None)

# 	if forms.is_valid():
# 		forms.kode_nota =kode_nota
# 		print(forms.kode_nota)
# 		form.save()
# 		return redirect('shop-list')
# 	context = {
# 		'form':forms,
# 		'kode_nota':kode_nota,
# 	}
# 	template = 'shop/pembayarancreate.html'
# 	return render(request, template, context)

class OrderUpdateView(UpdateView):
	model = Order
	template_name = 'shop/checkout_page.html'
	# template_name = 'shop/form.html'
	form_class = OrderUpdateForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		url = "https://pro.rajaongkir.com/api/province"
		headers = { 'key': settings.API_KEY_SECRET }
		r = requests.get(url, headers)
		provinces = r.json()
		context['provinces'] = provinces
		obj = super(OrderUpdateView, self).get_object(queryset = Order.objects.filter(status_order = False))
		if obj.bukti_pembayaran:
			obj.status_order = True
			obj.save()
		return context

	def get_success_url(self, **kwargs):
		return reverse('shop-bayar', kwargs={'pk':self.object.id})


class OrderBayarUpdateView(UpdateView):
	model = Order
	template_name = 'shop/bayar.html'
	form_class = OrderBayarForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['users'] = self.request.user
		context['bayar'] = Order.objects.filter(user = self.request.user, status_order = False)
		obj = super(OrderBayarUpdateView, self).get_object(queryset = context['bayar'])
		print("obj = ", obj)
		print(obj.bukti_pembayaran)
		if obj.bukti_pembayaran:
			obj.status_order = True
			print(obj.status_order)
			obj.save()
			print(obj.status_order)
		
		return context

	def get_success_url(self, **kwargs):
		return reverse('shop-list')

def order_update(request, pk):
	url = "https://pro.rajaongkir.com/api/province"
	headers = { 'key': settings.API_KEY_SECRET }
	r = requests.get(url, headers)
	provinces = r.json()
	template = 'shop/form.html'
	order = get_object_or_404(Order, pk=pk)
	form = OrderUpdateForm(request.POST or None, instance=order)
	if form.is_valid():
		form.save()
		return redirect('shop-list')

	context = {
    	'form':form,
		'provinces':provinces,
	}
	return render(request, template, context)

def orderitem_update(self, pk):
	ord_item = get_object_or_404(OrderItem, pk=pk)
	form = OrderItemForm(request.POST or None)
	
	if form.is_valid():
		form.save()
	
	context = {
		"form": form
		}
	return redirect(reverse('shop-checkout', kwargs = {'id':self.pk}))
	# return redirect('/')

class OrderItemUpdateView(UpdateView):
	model = OrderItem
	form_class = OrderItemForm
	# queryset = OrderItem.objects.filter(order__status_order = False)
	# success_url = reverse_lazy('shop-list')

	def get_success_url(self):
		return reverse_lazy('shop-checkout', kwargs={'pk':self.object.order.id})


