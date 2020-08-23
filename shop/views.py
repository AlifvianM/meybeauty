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
from .forms import PembayaranForm, OrderUpdateForm,OrderBayarForm, OrderItemForm, OrderItemForm2, MemberForm, OrderResiForm, ResellerForm
from rajaongkir import RajaOngkirApi
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse

import http.client
import requests
import datetime
import json

from django.core.paginator import Paginator

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import send_mail


# Create your views here.


def cek_ongkir(request,kota_id, kecamatan_tujuan_id, berat, jasa_ongkir):
	kota_id = kota_id
	kecamatan_tujuan_id = kecamatan_tujuan_id
	berat = berat
	jasa_ongkir = jasa_ongkir
	url = "https://pro.rajaongkir.com/api/cost"  #origin=501&originType=city&destination=574&destinationType=subdistrict&weight=1700&courier=jne
	payload = "origin=" + kota_id + "&originType=city&destination=" + kecamatan_tujuan_id + "&destinationType=subdistrict&weight=" + str(berat) + "&courier=" + jasa_ongkir
	r = requests.post(url,payload, headers = { 'key': settings.API_KEY_SECRET, 'content-type': "application/x-www-form-urlencoded" })
	ongkir = r.json()
	context = {
		'ongkir':ongkir,
		'kota_asal':kota_id,
		'kecamatan_tujuan':kecamatan_tujuan_id,

	}

	return render(request, 'shop/ongkir.html', context)




def cek_kecamatan_tujuan(request, kota_tujuan_id):
	kota_tujuan_id = kota_tujuan_id
	url = "https://pro.rajaongkir.com/api/subdistrict?city=" + str(kota_tujuan_id)
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

	context = {
		'city':kota,

	}
	return render(request, 'shop/kota_tujuan.html', context)

def cek_kota(request, prov_id):
	prov_id = prov_id
	url = "https://pro.rajaongkir.com/api/city?province=" + prov_id
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
	pl = Product.objects.all().order_by('-created_at')

	context = {
		'products' : pl,
	}
	return render(request, 'shop/dashboard.html', context)


def product_list(request):
	if request.user.is_active:
		pl = Product.objects.all().order_by('-created_at')
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
			# 'title':'DRWSkincare Banyuwangi',
			'form':form,
			}
	else:
		pl = Product.objects.all().order_by('-created_at')
		form = OrderItemForm(request.POST or None)

		if form.is_valid():
			form.save()
			return redirect(reverse('shop-checkout', kwargs = {'id':self.items.order.id}))

		context = {
			'products' : pl,
			'form':form,
			# 'title':'DRWSkincare Banyuwangi',
			}

	template = 'shop/home.html'
	return render(request, template, context)

def product_detail(request, slug):
	obj = get_object_or_404(Product, slug=slug)
	count_items = OrderItem.objects.filter(order__status_order = False).aggregate(Count('id'))['id__count'] or 0
	product = Product.objects.all().order_by('-created_at')
	context = {
		'obj':obj,
		'count_items':count_items,
		'product':product,
		'title':obj.nama,
	}
	template = 'shop/product-details.html'
	return render(request, template, context)


@login_required
def add_to_cart(request,pk):
	pk = pk
	now = datetime.datetime.now()
	product = get_object_or_404(Product, pk=pk)
	cart,created = Order.objects.get_or_create(
        user=request.user,
        status_order = False,
         )
	orderitem,created = OrderItem.objects.get_or_create(product=product,order=cart, price=product.harga, total_weight=product.berat)
	total = OrderItem.objects.filter(order__status_order = False).aggregate(Sum('price'))['price__sum'] or 0.00
	if created:
		kode = 'INV'+now.strftime('%Y')+now.strftime('%m')+now.strftime('%d')+str(orderitem.order.pk)
		orderitem.order.kode_nota = kode
		orderitem.order.harga = total
		orderitem.save()
		cart.save()
	messages.success(request, "Cart updated!")
	return redirect('shop-showcart')


# 2020-06-06 05:24:29.900785

@login_required
def delete_from_cart(request, **kwargs):
    item_to_delete = OrderItem.objects.filter(product__slug=kwargs['slug'])
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect('shop-showcart')

@login_required
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


@login_required
def orderupdate(request, kode_nota):
	order = get_object_or_404(Order, kode_nota=kode_nota)
	form = OrderUpdateForm(request.POST or None, instance = order)
	url = "https://pro.rajaongkir.com/api/province"
	headers = { 'key': settings.API_KEY_SECRET }
	items = OrderItem.objects.filter(order__user = request.user or None, order__status_order = False)
	sum_price_item = OrderItem.objects.filter(order__user = request.user or None, order__status_order = False).aggregate(Sum('total_harga'))['total_harga__sum'] or 0.00
	sum_weight_item = OrderItem.objects.filter(order__user = request.user or None, order__status_order = False).aggregate(Sum('total_weight'))['total_weight__sum'] or 0.00
	order.harga = sum_price_item
	order.berat = sum_weight_item
	order.save()
	r = requests.get(url, headers)
	provinces = r.json()

	if form.is_valid():
		orderitem = OrderItem.objects.filter(order__kode_nota = order.kode_nota)
		order.total_harga = order.harga + order.harga_ongkir
		order.status_order = True
		order.save()
		form.save()
		user = request.user
		to_email = user.email
		message = render_to_string('shop/order_email.html', {
                'user': user,
                'order':order,
                'orderitem':orderitem,
                # 'domain': current_site.domain,
                # 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                # 'token':account_activation_token.make_token(user),
                })
		mail_subject = 'Menunggu Pembayaran Anda'
# 		email = EmailMessage(mail_subject, message, to=[to_email])
# 		email.send()
		send_mail(
		    subject = mail_subject,
		    message = message,
		    from_email = settings.EMAIL_HOST_USER,
		    recipient_list = [to_email],
		    fail_silently = False,
		)
			# return redirect(reverse('shop-list'))
		return redirect(reverse('shop-orderdetail', kwargs={'kode_nota':kode_nota}))

	context = {
		'order':order,
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
		if obj.bukti_pembayaran:
			obj.status_order = True
			obj.save()		
		return context

	# def form_valid(self, form):
	# 	Order.objects.filter(pk = self.id).update(status_order = True)
	# 	return super().form_valid(form)

	def get_success_url(self, **kwargs):
		return reverse('shop-list')

@login_required
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

@login_required
def orderitem_update(request, order_id):
			
	
	context = {
		"form": form
		}
	return redirect(reverse('shop-checkout', kwargs = {'pk':order_id}))

@login_required
def updateorderitem(request, value, pk_orderitem):
	orderitem = get_object_or_404(OrderItem, pk = pk_orderitem)
	OrderItem.objects.filter(order__user = request.user, order__status_order = False, pk = pk_orderitem).update(quantity=value)
	oi = OrderItem.objects.get(pk = pk_orderitem, order__status_order = False, order__user = request.user)
	oi.total_harga = value * oi.price
	oi.total_weight = value * oi.product.berat
	OrderItem.objects.filter(order__user = request.user, order__status_order = False, pk = pk_orderitem).update(total_harga=oi.total_harga, total_weight = oi.total_weight)
	return HttpResponse(value)

class OrderItemUpdateView(UpdateView):
	model = OrderItem
	form_class = OrderItemForm
	def form_valid(self, form):
		qty = request.POST.getlist('quantity')
		self.object.order_set.update(quantity =qty )

	def get_success_url(self):
		return reverse('shop-checkout', kwargs={'pk':object.order.id})

@login_required
def transaction(request):
	order = Order.objects.filter( user = request.user, status_order=True).order_by('-created_at')
	count_items = OrderItem.objects.filter(order__user = request.user, order__status_order = False).aggregate(Count('id'))['id__count'] or 0
	context = {
		'orders':order,
		'count_items':count_items
	}
	return render(request, 'shop/transaction.html', context)

@login_required
def OrderBayarUpdate(request, pk):
	order = get_object_or_404(Order, pk=pk)
	form = OrderBayarForm(request.POST, request.FILES, instance = order)
	form.kode_nota = order.kode_nota
	items = OrderItem.objects.filter(order__pk = pk, order__user = request.user)
	orders = Order.objects.filter(pk = pk, user = request.user)
	if form.is_valid():
		form.save()
		Order.objects.filter(pk = pk).update(status_bayar = 'SUDAH', status_order = True)
		orderitem = OrderItem.objects.filter(order__kode_nota = order.kode_nota)
		user = request.user
		to_email = user.email
		message = render_to_string('shop/bayar_email.html', {
                'user': user,
                'order':order,
                'orderitem':orderitem,
                })
		mail_subject = 'Pembayaran Berhasil'
		send_mail(
		    subject = mail_subject,
		    message = message,
		    from_email = settings.EMAIL_HOST_USER,
		    recipient_list = [to_email],
		    fail_silently = False,
		)
		return redirect(reverse('shop-orderdetail', kwargs={'pk':pk}))
	context = {
		'orders':orders,
		'items':items,
		'form':form,
	}		
	return render(request, 'shop/bayar.html', context)

@login_required
def orderdetail(request, kode_nota):
	order = get_object_or_404(Order, kode_nota=kode_nota)
	
	kota_id = order.kota_asal
	kecamatan_tujuan_id = order.kecamatan_tujuan
	berat = order.berat
	jasa_ongkir = order.jasa_ongkir
	url = "https://pro.rajaongkir.com/api/cost"  #origin=501&originType=city&destination=574&destinationType=subdistrict&weight=1700&courier=jne
	payload = "origin=" + kota_id + "&originType=city&destination=" + kecamatan_tujuan_id + "&destinationType=subdistrict&weight=" + str(berat) + "&courier=" + jasa_ongkir
	r = requests.post(url,payload, headers = { 'key': settings.API_KEY_SECRET, 'content-type': "application/x-www-form-urlencoded" })
	ongkir = r.json()
		
	waybill_url = "https://pro.rajaongkir.com/api/waybill"
	waybill_payload = "waybill="+order.resi+"&courier="+order.jasa_ongkir
	waybill_r = requests.post(waybill_url,waybill_payload, headers = { 'key': settings.API_KEY_SECRET, 'content-type': "application/x-www-form-urlencoded" })
	waybill = waybill_r.json()

	orderitem = OrderItem.objects.filter(order__kode_nota = order.kode_nota)
	count_items = OrderItem.objects.filter(order__user = request.user, order__status_order = False).aggregate(Count('id'))['id__count'] or 0
	
	orderitem = OrderItem.objects.filter(order__kode_nota = order.kode_nota)
	count_items = OrderItem.objects.filter(order__user = request.user, order__status_order = False).aggregate(Count('id'))['id__count'] or 0
	context = {
			'orders':order,
			'items':orderitem,
			'count_items':count_items,
			'ongkir':ongkir,
			'waybill':waybill,
		}
	return render(request, 'shop/order_detail.html', context)

# @login_required
def show_product(request):
	if request.user.is_active:	
		product = Product.objects.all().order_by('-created_at')
		count_items = OrderItem.objects.filter(order__user = request.user, order__status_order = False).aggregate(Count('id'))['id__count'] or 0
		paginator = Paginator(product, 20)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		context = {
			'products':product,
			'count_items':count_items,
			'page_obj':page_obj
		}
	else:
		product = Product.objects.all().order_by('-created_at')
		paginator = Paginator(product, 20)
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		context = {
			'products':product,
			# 'count_items':count_items,
			'page_obj':page_obj
		}
	return render(request, 'shop/products.html', context)


def show_product_home(request):
	product = Product.objects.all().order_by('-created_at')
	paginator = Paginator(product, 20)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context = {
		'products':product,
		'page_obj':page_obj
	}
	return render(request, 'shop/products.html', context)


def member(request):
	if request.POST:
		form = MemberForm(request.POST)
		if form.is_valid():
			form.save()
			user = form.cleaned_data.get('nama')
			to_email = form.cleaned_data.get('email')
			message = render_to_string('shop/member_email.html', {
                'user': user,
                })
			mail_subject = 'Thanks For Being Member Of DRWSkincare Banyuwangi.'
			# email = EmailMessage(mail_subject, message, to=[to_email])
			# email.send()
			send_mail(
			    subject = mail_subject,
			    message = message,
			    from_email = settings.EMAIL_HOST_USER,
			    recipient_list = [to_email],
			    fail_silently = False,
			)
			return redirect(reverse('shop-list'))
	else:
		form = MemberForm()
	return render(request, 'shop/member.html', {'form':form, 'title':'Join Member'})

def search(request):
	template = 'shop/products.html'
	query = request.GET.get('q', None)
	if query:
		product = Product.objects.filter(Q(nama__icontains = query)).order_by('-created_at')
	else:
		product = Product.objects.all()

	paginator = Paginator(product, 20)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context = {
		'products':product,
		'page_obj':page_obj,
	}
	return render(request, template, context)


def updateresi(request, pk):
	if request.user.is_superuser:
		resi = get_object(Order, pk = pk)
		form = OrderResiForm(request.POST)
		if form.is_valid():
			resi = form.cleaned_data.get('resi')
			to_email = resi.user.email
			message = render_to_string('shop/resi_email.html', {
                'user': user,
                'resi': resi,
                })
			mail_subject = 'Nomor Resi Pesanan Anda Telah Ditambahkan.'
			# email = EmailMessage(mail_subject, message, to=[to_email])
			# email.send()
			send_mail(
			    subject = mail_subject,
			    message = message,
			    from_email = settings.EMAIL_HOST_USER,
			    recipient_list = [to_email],
			    fail_silently = False,
			)
		else:
			resi = OrderResiForm()
		context = {
			'form':OrderResiForm()
		}
		return render(request, 'shop/bayar.html', context)
	else:
		return redirect(reverse('shop-list'))


def	all_transaction(request):
	if request.user.is_superuser:
		order = Order.objects.all().order_by('-created_at')
		context = {
			'order':order,
		}
		return render(request, 'shop/transaction.html', context)
	else:
		return redirect(reverse('shop-list'))


def reseller(request):
	if request.POST:
		form = ResellerForm(request.POST)
		if form.is_valid():
			form.save()
			user = form.cleaned_data.get('nama')
			to_email = form.cleaned_data.get('email')
			message = render_to_string('shop/member_email.html', {
                'user': user,
                })
			mail_subject = 'Thanks For Being Reseller Of DRWSkincare Banyuwangi.'
			send_mail(
			    subject = mail_subject,
			    message = message,
			    from_email = settings.EMAIL_HOST_USER,
			    recipient_list = [to_email],
			    fail_silently = False,
			)
			return redirect(reverse('shop-list'))
		else:
			return redirect(reverse('shop-reseller'))
	else:
		form = ResellerForm()
	context = {
		'form':form,
		'title':'Join Reseller'
	}
	return render(request, 'shop/member.html', context)




