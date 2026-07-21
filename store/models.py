from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    nama = models.CharField(max_length=100)

    def __str__(self):
        return self.nama


class Product(models.Model):
    nama = models.CharField(max_length=200)
    kategori = models.ForeignKey(Category, on_delete=models.CASCADE)
    harga = models.IntegerField()
    stok = models.IntegerField()
    deskripsi = models.TextField()
    gambar = models.ImageField(upload_to='produk/')
    diskon = models.IntegerField(default=0)
    rating = models.FloatField(default=5)

    @property
    def harga_diskon(self):
        if self.diskon > 0:
            return self.harga - (self.harga * self.diskon / 100)
        return self.harga

    def __str__(self):
        return self.nama

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produk = models.ForeignKey(Product, on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField(default=1)
    dibuat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.produk.nama}"
    
    @property
    def subtotal(self):
        return self.produk.harga_diskon * self.jumlah

class Order(models.Model):

    STATUS = (
        ('Menunggu Pembayaran', 'Menunggu Pembayaran'),
        ('Menunggu Verifikasi', 'Menunggu Verifikasi'),
        ('Diproses', 'Diproses'),
        ('Dikirim', 'Dikirim'),
        ('Selesai', 'Selesai'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    telepon = models.CharField(max_length=20)
    alamat = models.TextField()

    metode_pembayaran = models.CharField(max_length=50)

    bukti_pembayaran = models.ImageField(
        upload_to='bukti/',
        blank=True,
        null=True
    )

    total = models.DecimalField(max_digits=12, decimal_places=2)

    status = models.CharField(
        max_length=30,
        choices=STATUS,
        default='Menunggu Pembayaran'
    )

    dibuat = models.DateTimeField(auto_now_add=True)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    produk = models.ForeignKey(Product, on_delete=models.CASCADE)
    jumlah = models.PositiveIntegerField(default=1)
    harga = models.DecimalField(max_digits=12, decimal_places=2)

    def subtotal(self):
        return self.jumlah * self.harga

    def __str__(self):
        return self.produk.nama
    
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    dibuat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produk = models.ForeignKey(Product, on_delete=models.CASCADE)
    dibuat = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'produk')

    def __str__(self):
        return f"{self.user.username} - {self.produk.nama}"
    

class Contact(models.Model):
    nama = models.CharField(max_length=100)
    email = models.EmailField()
    pesan = models.TextField()
    dibuat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama
    
class ContactMessage(models.Model):
    nama = models.CharField(max_length=100)
    email = models.EmailField()
    pesan = models.TextField()
    dibuat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama