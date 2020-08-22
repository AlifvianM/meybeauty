from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from shop.models import Order, Product, Reseller, Member
from django.shortcuts import get_object_or_404
from .forms import OrderForm, ProductForm, MemberForm
from django.urls import reverse, reverse_lazy
from django.db.models import Avg, Sum, Count
from django.contrib import messages

from datetime import date
from django.template.loader import render_to_string
from django.views.generic import ListView,DetailView
from django.conf import settings
from django_weasyprint import WeasyTemplateResponseMixin
from django_weasyprint.views import CONTENT_TYPE_PNG
import io
from django.http import FileResponse, HttpResponse
from reportlab.pdfgen import canvas
from django.core.mail import send_mail
# Create your views here.


@login_required
def index(request):
	order = Order.objects.all().order_by('-created_at')
	total_harga = Order.objects.all().aggregate(Sum('total_harga'))['total_harga__sum'] or 0
	total_pending = Order.objects.filter(status_order = False).aggregate(Sum('total_harga'))['total_harga__sum'] or 0
	total_id = Order.objects.filter(status_order = True).aggregate(Count('kode_nota'))['kode_nota__count'] or 0
	total_id_pending = Order.objects.filter(status_order = False).aggregate(Count('kode_nota'))['kode_nota__count'] or 0
	context = {
		'orders':order,
		'total_harga':total_harga,
		'total_pending':total_pending,
		'total_id':total_id,
		'total_id_pending':total_id_pending,
		'title':'Dashboard',

	}
	return render(request, 'adminpage/home.html', context)


@login_required
def updateresi(request, kode_nota):
	order = get_object_or_404(Order, kode_nota = kode_nota)
	form = OrderForm(request.POST, instance = order)
	print(form)
	if form.is_valid():
		form.save()
		user = order.user
		to_email = user.email
		resi = order.resi
		message = render_to_string('adminpage/resi_email.html', {
                'user': user,
                'resi':resi,
                'kode_nota':order.kode_nota
                })
		mail_subject = 'Resi Pemesanan Anda'
		send_mail(
		    subject = mail_subject,
		    message = message,
		    from_email = 'printdisini2020@gmail.com',
		    recipient_list = [to_email],
		    fail_silently = False,
		)
		return redirect(reverse('adminpage-index'))
	context = {
		'order':order,
		'form':form,
		'title':'Add Shipment Code'
	}
	return render(request, 'adminpage/formresi.html', context)

def pdf_generate(request):
	buffer = io.BytesIO()
	p = canvas.Canvas(buffer)
	p.drawString(100, 100, "Hello world.")
	p.showPage()
	p.save()

	return FileResponse(buffer, as_attachment=False, filename='hello.pdf')

class OrderListView(ListView):
	model = Order
	template_name = 'adminpage/pdf.html'
	queryset = Order.objects.filter(status_order=True)
	context_object_name = 'pesans'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['today'] = date.today()
		context['total_pesan']= Order.objects.filter(status_order = True).aggregate(Count('kode_nota'))['kode_nota__count'] or 0
		context['total_harga']= Order.objects.all().aggregate(Sum('total_harga'))['total_harga__sum'] or 0
		
		return context

class MyModelDownloadView(WeasyTemplateResponseMixin, OrderListView):
	pdf_attachment = False
	pdf_filename = 'list.html'


def add_product(request):
	form = ProductForm()
	if request.POST:
		form = ProductForm(request.POST, request.FILES)
		print(form.is_valid())
		if form.is_valid():
			form.save()
			return redirect(reverse('adminpage-list_product'))
		else:
			# return redirect(reverse('adminpage-product'))
			return HttpResponse("SALAH")
	else:
		form = ProductForm()
	context = {
		'form':form,
		'title':'Add Product',
	}
	return render(request, 'adminpage/formproduct.html', context)
		

@login_required
def list_product(request):
	product = Product.objects.all().order_by('-created_at')
	context = {
		'products':product,
		'title':'List Product'
	}
	return render(request, 'adminpage/listproduct.html', context)


@login_required
def delete_product(request, pk):
	if request.user.is_superuser:
		product = Product.objects.filter(pk = pk)
		if product.exists():
			product.delete()
			messages.info(request, 'Item Has Been Deleted')
			return redirect(reverse('adminpage-list_product'))
		else:
			messages.danger(request, 'Item Cant Be Deleted')
			return redirect(reverse('adminpage-list_product'))
	else:
		return redirect(reverse('adminpage-index'))


def order_detail(request, kode_nota):
	order = get_object_or_404(Order, kode_nota=kode_nota)
	context = {
		'order':order
	}
	return render(request, 'adminpage/order_detail.html', context)

@login_required
def list_reseller(request):
	reseller = Reseller.objects.all().order_by('-created_at')
	context = {
		'resellers':reseller,
		'title':'List Reseller',
	}
	return render(request, 'adminpage/listreseller.html', context)


@login_required
def list_member(request):
	if request.user.is_superuser:
		member = Member.objects.all().order_by('-created_at')
		context = {
			'members':member,
			'title':'List Member',
		}
	else:
		return redirect('shop-index')
	return render(request, 'adminpage/listmember.html', context)

@login_required
def updatemember(request, pk):
	member = get_object_or_404(Member, pk=pk)
	if request.POST:
		form = MemberForm(request.POST, instance=member)
		print(form)
		if form.is_valid():
			form.save()
			return redirect(reverse('adminpage-list_member'))
		else:
			return HttpResponse("DATA SALAH")
	else:
		form = MemberForm()
	context = {
		'form':form,
		'title':'Update Member'
	}
	return render(request, 'adminpage/updatemember.html', context)



