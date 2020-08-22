from django.urls import path
from .views import (
	index, 
	updateresi,
	add_product,
	MyModelDownloadView,
	list_product,
	order_detail,
	list_reseller,
	list_member,
	delete_product,
	updatemember,
	)

urlpatterns = [
	path('member/<int:pk>/update', updatemember, name='adminpage-memberupdate'),
	path('list_member', list_member, name='adminpage-list_member'),
	path('list_reseller', list_reseller, name='adminpage-list_reseller'),
	path('detail/<str:kode_nota>', order_detail, name='adminpage-detail'),
	path('delete/product/<int:pk>/', delete_product, name='adminpage-delete_product'),
	path('listproduct', list_product, name='adminpage-list_product'),
	path('product/tambah', add_product, name='adminpage-product'),
	path('pdf',MyModelDownloadView.as_view(), name = 'pdf'),
	path('tambahresi/<str:kode_nota>', updateresi, name='adminpage-resi'),
	path('', index, name='adminpage-index'),
]