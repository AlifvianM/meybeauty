from django.urls import path
from .views import (
	product_list,
	product_detail,
	add_to_cart,
	show_cart,
	delete_from_cart,
	# pembayarancreate,
	cek_provinsi,
	cek_kota,
	cek_kota_tujuan,
	cek_kecamatan_tujuan,
	cek_ongkir,
	OrderUpdateView,
	order_update,
	OrderBayarUpdateView,
	OrderItemDeleteView,
	orderitem_update,
	OrderItemUpdateView,
	orderupdate,
	OrderBayarUpdate,
	updateorderitem, # update order item js
	dashboard,
	transaction,
	orderdetail,
	show_product,
	show_product_home,
	member,
	search,
	)

from django.conf.urls.static import static
from django.conf import settings



urlpatterns= [
	path('search', search, name='shop-search'),
	path('member', member, name='shop-member'),
	path('orderdetail/<int:pk>', orderdetail, name='shop-orderdetail'),
	path('transaction/', transaction, name = 'shop-transaction'),
	path('bayar/<int:pk>', OrderBayarUpdate, name='shop-bayar'),
	path('cek_ongkir/<str:kota_id>/<str:kecamatan_tujuan_id>/<int:berat>/<str:jasa_ongkir>', cek_ongkir, name='cek_ongkir'),
	path('cek_kecamatan_tujuan/<str:kota_tujuan_id>', cek_kecamatan_tujuan, name='cek_kecamatan_tujuan'),
	path('cek_kota_tujuan/<str:prov_tujuan_id>', cek_kota_tujuan, name='cek_kota'),
	path('cek_kota/<str:prov_id>', cek_kota, name='cek_kota'),
	path('cek_provinsi', cek_provinsi, name='cek_provinsi'),
	# path('CheckOut/<int:pk>', OrderUpdateView.as_view(), name='shop-checkout'),
	path('CheckOut/<int:pk>', orderupdate, name='shop-checkout'),
	path('homecheck/<int:order_id>', orderitem_update, name='shop-homecheck'),
	# path('CheckOut/<str:kode_nota>', pembayarancreate, name='shop-checkout'),
	path('orderitemupdate/<int:value>/<int:pk_orderitem>', updateorderitem, name='shop-orderitem'),
	path('cart', show_cart, name='shop-showcart'),
	path('delete_from_cart/<int:pk>', OrderItemDeleteView.as_view(), name='shop-deletecart'),
	path('add-to-cart/<int:pk>', add_to_cart, name='shop-addcart'),
	path('detail/<slug:slug>', product_detail, name='shop-detail'),
	path('dashboard', product_list, name = 'shop-list'),
	path('products', show_product, name = 'show_product'),
	path('product', show_product_home, name = 'show_product_home'),
	path('', dashboard, name = 'shop-dashboard'),
]