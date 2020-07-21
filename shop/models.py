from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from datetime import datetime
from users.models import Profile

class Product(models.Model):
    nama = models.CharField(max_length=120)
    harga = models.IntegerField()
    foto = models.ImageField(upload_to='documents/', null=True)
    slug  = models.SlugField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    # created = models.DateTimeField(auto_now_add=True)
    # category

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nama)
        return super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.nama




class Order(models.Model):
    STATUS = (
            ('SUDAH','sudah'),
            ('BELUM','belum'),
        )
    kode_nota = models.CharField(max_length=255)
    status_order = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    harga = models.FloatField(blank=True, null=True)
    provinsi_asal = models.CharField(max_length=255, default='11')
    kota_asal = models.CharField(max_length=255, default='42')
    kecamatan_asal = models.CharField(max_length=255, default='611')
    provinsi_tujuan = models.CharField(max_length=255, null=True, blank=True)
    kota_tujuan = models.CharField(max_length=255, null=True, blank=True)
    kecamatan_tujuan = models.CharField(max_length=255, null=True, blank=True)
    jasa_ongkir = models.CharField(max_length=50, default='jne')
    harga_ongkir = models.FloatField(default=0)
    total_harga = models.FloatField(default=0)
    bukti_pembayaran = models.ImageField(upload_to='bukti/', null=True, blank=True)
    status_bayar = models.CharField(max_length=50, choices=STATUS, default='BELUM')
    alamat = models.TextField()
    resi = models.CharField(max_length=255, null=True, blank=True, default='Menunggu nomor resi')

    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return "kode_nota {}".format(self.kode_nota)
    # def save(self, *args, **kwargs):
    #     if self.bukti_pembayaran:
    #         self.status_order = True
    #     super(Order, self).save(*args, **kwargs)

class OrderItem(models.Model):
    # kode_nota
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(null=True)
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, null=True)
    price = models.FloatField(null=True)
    quantity = models.IntegerField(default=1)
    total_harga = models.FloatField(default=0)

    def __str__(self):
        # return "ID ORDER ITEM {}".format(self.id)
        return self.product.nama

    def save(self, *args, **kwargs):
        self.total_harga = self.quantity * self.price
        super(OrderItem, self).save(*args, **kwargs)


class Pembayaran(models.Model):
    bukti_pembayaran = models.ImageField(upload_to='bukti/')
    kode_nota = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    # provinsi_asal = models.CharField(max_length=255, default='11')
    # # kota_asal = models.CharField(max_length=255, default='42')
    # kecamatan_asal = models.CharField(max_length=255, default='611')
    # provisi_tujuan = models.CharField(max_length=255)
    # kota_tujuan = models.CharField(max_length=255)
    # kecamatan_tujuan = models.CharField(max_length=255)
    # jasa_ongkir = models.CharField(max_length=50, default='jne')
    # harga_ongkir = models.FloatField(default=0)

    def __str__(self):
        return "Nota {}. ID {}.".format(self.kode_nota.kode_nota, self.id)

class Member(models.Model):
    nama            = models.CharField(max_length=50)
    email           = models.EmailField(max_length=254)
    nomor_telepon   = models.CharField(max_length=50)
    terms           = models.BooleanField(default=False)


