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
from .forms import PembayaranForm, OrderUpdateForm,OrderBayarForm, OrderItemForm, OrderItemForm2, MemberForm
from rajaongkir import RajaOngkirApi

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse

import http.client
import requests
import datetime
import json

from django.core.paginator import Paginator

from django.template.loader import render_to_string
from django.core.mail import EmailMessage



# Create your views here.


def cek_ongkir(request,kota_id, kecamatan_tujuan_id, berat, jasa_ongkir):
	kota_id = kota_id
	kecamatan_tujuan_id = kecamatan_tujuan_id
	berat = berat
	jasa_ongkir = jasa_ongkir
	conn = http.client.HTTPConnection("pro.rajaongkir.com")
	url = "https://pro.rajaongkir.com/api/cost"  #origin=501&originType=city&destination=574&destinationType=subdistrict&weight=1700&courier=jne
	# print(url)
	payload = "origin=" + kota_id + "&originType=city&destination=" + kecamatan_tujuan_id + "&destinationType=subdistrict&weight=" + str(berat) + "&courier=" + jasa_ongkir
	
	r = requests.post(url,payload, headers = { 'key': settings.API_KEY_SECRET, 'content-type': "application/x-www-form-urlencoded" })
	# r = conn.request("POST","/api/cost",payload, headers = { 'key': settings.API_KEY_SECRET, 'content-type': "application/x-www-form-urlencoded" })
	
	ongkir = r.json()

	# for o in ongkir.values():
	# 	print(o['results'])
	# print(json.dumps(ongkir, indent=2))

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

def dashboard(request):
	pl = Product.objects.all()

	context = {
		'products' : pl,
	}
	return render(request, 'shop/dashboard.html', context)

@login_required
def product_list(request):
	pl = Product.objects.all()
	items = OrderItem.objects.filter(order__user = request.user or None, order__status_order = False)
	total = OrderItem.objects.filter(order__user = request.user or None, order__status_order = False).aggregate(Sum('price'))['price__sum'] or 0.00
	count_items = OrderItem.objects.filter(order__user = request.user, order__status_order = False).aggregate(Count('id'))['id__count'] or 0
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
	count_items = OrderItem.objects.filter(order__status_order = False).aggregate(Count('id'))['id__count'] or 0
	context = {
		'obj':obj,
		'count_items':count_items,
	}
	template = 'shop/product-details.html'
	return render(request, template, context)


@login_required
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
    return redirect('shop-showcart')


# 2020-06-06 05:24:29.900785


def delete_from_cart(request, **kwargs):
    item_to_delete = OrderItem.objects.filter(product__slug=kwargs['slug'])
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect('shop-showcart')

def show_cart(request):
	items = OrderItem.objects.filter(order__user = request.user, order__status_order = False)
	order = Order.objects.filter(user = request.user, status_order=False)
	all_items = OrderItem.objects.filter(order__user = request.user)
	total = OrderItem.objects.filter(order__user = request.user, order__status_order = False).aggregate(Sum('price'))['price__sum'] or 0.00
	count_items = OrderItem.objects.filter(order__user = request.user, order__status_order = False).aggregate(Count('id'))['id__count'] or 0
	context = {
		'orders':order,
		'items':items,
		'item_true':all_items,
		'total':total,
		'count_items':count_items,
	}
	return render(request, 'shop/cart.html', context)

class OrderItemDeleteView(DeleteView):
    model = OrderItem
    # template_name = "shop/delete.html"


    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('shop-showcart')

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
		obj = super(OrderUpdateView, self).get_object(queryset = OrderItem.objects.filter(order__status_order = False))
		if obj.bukti_pembayaran:
			obj.status_order = True
			obj.save()
		return context

	def get_success_url(self, **kwargs):
		return reverse('shop-bayar', kwargs={'pk':self.object.id})


def orderupdate(request, pk):
	order = get_object_or_404(Order, pk=pk)
	form = OrderUpdateForm(request.POST or None, instance = order)
	url = "https://pro.rajaongkir.com/api/province"
	headers = { 'key': settings.API_KEY_SECRET }
	items = OrderItem.objects.filter(order__user = request.user or None, order__status_order = False)
	sum_price_item = OrderItem.objects.filter(order__user = request.user or None, order__status_order = False).aggregate(Sum('total_harga'))['total_harga__sum'] or 0.00
	print("order :", order.total_harga)
	order.harga = sum_price_item
	order.save()

	r = requests.get(url, headers)
	provinces = r.json()
	if form.is_valid():
		order.total_harga = order.harga + order.harga_ongkir
		# order.status_order = True
		order.save()
		form.save()
		return redirect(reverse('shop-orderdetail', kwargs={'pk':pk}))

	context = {
		'total':sum_price_item,
		'form':form,
		'provinces':provinces,
		'items':items,
	}
	return render(request, 'shop/checkout_page.html', context)



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

	# def form_valid(self, form):
	# 	Order.objects.filter(pk = self.id).update(status_order = True)
	# 	return super().form_valid(form)

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
	orderitem = OrderItem.objects.filter(order__pk = pk, status_order = False, order__user = request.user)


	if form.is_valid():
		
		form.save()
		return redirect('shop-list')

	context = {
    	'form':form,
		'provinces':provinces,
	}
	return render(request, template, context)

# def orderitem_update(request, pk):
# 	ord_item = get_object_or_404(OrderItem, pk=pk)
# 	form = OrderItemForm(request.POST or None)
	
# 	if form.is_valid():
# 		form.save()

	
# 	context = {
# 		"form": form
# 		}
# 	return redirect(reverse('shop-checkout', kwargs = {'pk':pk}))
	# return redirect('/')


def orderitem_update(request, order_id):
			
	
	context = {
		"form": form
		}
	return redirect(reverse('shop-checkout', kwargs = {'pk':order_id}))


def updateorderitem(request, value, pk_orderitem):
	orderitem = get_object_or_404(OrderItem, pk = pk_orderitem)
	OrderItem.objects.filter(order__user = request.user, order__status_order = False, pk = pk_orderitem).update(quantity=value)
	oi = OrderItem.objects.get(pk = pk_orderitem, order__status_order = False, order__user = request.user)
	print("quantity : ", oi.quantity)
	oi.total_harga = oi.quantity * oi.price
	print('harga :', oi.total_harga)
	OrderItem.objects.filter(order__user = request.user, order__status_order = False, pk = pk_orderitem).update(total_harga=oi.total_harga)

	return HttpResponse(value)

class OrderItemUpdateView(UpdateView):
	model = OrderItem
	form_class = OrderItemForm
	# queryset = OrderItem.objects.filter(order__status_order = False)
	# success_url = reverse_lazy('shop-list')

	# def post(self, request, *args, **kwargs):
	# 	self.object = self.get_object()
	# 	return super().post(request, *args, **kwargs)
	def form_valid(self, form):
		qty = request.POST.getlist('quantity')
		self.object.order_set.update(quantity =qty )

	def get_success_url(self):
		return reverse('shop-checkout', kwargs={'pk':object.order.id})

def transaction(request):
	order = Order.objects.filter( user = request.user).order_by('-created_at')
	count_items = OrderItem.objects.filter(order__user = request.user, order__status_order = False).aggregate(Count('id'))['id__count'] or 0
	context = {
		'orders':order,
		'count_items':count_items
	}
	return render(request, 'shop/transaction.html', context)


# def transaction(request):
# 	order = Order.objects.filter(user = request.user, status_order = ).order_by('-created_at')



# def OrderBayarUpdate(request, pk):
# 	order = get_object_or_404(Order, pk=pk)
# 	form = OrderBayarForm(request.POST or None, instance = order)
# 	items = OrderItem.objects.filter(order__pk = pk, order__user = request.user)
# 	orders = Order.objects.filter(pk = pk, user = request.user)
# 	if form.is_valid():
# 		Order.objects.filter(pk = pk).update(status_order = True)
# 		return redirect(reverse('shop-list'))
# 	context = {
# 		'orders':orders,
# 		'items':items,
# 		'form':form,
# 	}		
# 	return render(request, 'shop/bayar.html', context)

def OrderBayarUpdate(request, pk):
	order = get_object_or_404(Order, pk=pk)
	form = OrderBayarForm(request.POST, request.FILES, instance = order)
	form.kode_nota = order.kode_nota
	print(form.kode_nota)
	items = OrderItem.objects.filter(order__pk = pk, order__user = request.user)
	orders = Order.objects.filter(pk = pk, user = request.user)
	if form.is_valid():
		form.save()
		Order.objects.filter(pk = pk).update(status_bayar = 'SUDAH', status_order = True)
		print("FOTO :",order.bukti_pembayaran)
		return redirect(reverse('shop-orderdetail', kwargs={'pk':pk}))
	context = {
		'orders':orders,
		'items':items,
		'form':form,
	}		
	return render(request, 'shop/bayar.html', context)

def orderdetail(request, pk):
	order = get_object_or_404(Order, pk=pk)
	orderitem = OrderItem.objects.filter(order__kode_nota = order.kode_nota)
	count_items = OrderItem.objects.filter(order__user = request.user, order__status_order = False).aggregate(Count('id'))['id__count'] or 0
	sum_price = order.harga + order.harga_ongkir 
	context = {
		'orders':order,
		'items':orderitem,
		'count_items':count_items,
		'total':sum_price
	}
	return render(request, 'shop/order_detail.html', context)

@login_required
def show_product(request):
	product = Product.objects.all().order_by('-created_at')
	count_items = OrderItem.objects.filter(order__user = request.user, order__status_order = False).aggregate(Count('id'))['id__count'] or 0
	paginator = Paginator(product, 1)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context = {
		'products':product,
		'count_items':count_items,
		'page_obj':page_obj
	}
	return render(request, 'shop/products.html', context)

def member(request):
	if request.POST:
		form = MemberForm(request.POST)
		if form.is_valid():
			user = form.cleaned_data.get('nama')
			to_email = form.cleaned_data.get('email')
			message = render_to_string('shop/member_email.html', {
                'user': user,
                # 'domain': current_site.domain,
                # 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                # 'token':account_activation_token.make_token(user),
                })
			mail_subject = 'Thanks For Being Member Of DRWSkincare Banyuwangi.'
			email = EmailMessage(mail_subject, message, to=[to_email])
			email.send()
			return redirect(reverse('shop-list'))
	else:
		form = MemberForm()
	return render(request, 'shop/member.html', {'form':form})



