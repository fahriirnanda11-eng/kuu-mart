from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategori"


class Product(models.Model):
    nama = models.CharField(max_length=200)

    kategori = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="produk"
    )

    deskripsi = models.TextField(blank=True, null=True)

    harga = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    diskon = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    stok = models.PositiveIntegerField(default=0)

    gambar = models.ImageField(
        upload_to="produk/",
        blank=True,
        null=True
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=5.0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5)
        ]
    )

    terjual = models.PositiveIntegerField(default=0)

    dibuat = models.DateTimeField(auto_now_add=True)
    diperbarui = models.DateTimeField(auto_now=True)

    @property
    def harga_diskon(self):
        if self.diskon > 0:
            return self.harga - (
                self.harga * self.diskon / 100
            )
        return self.harga

    def __str__(self):
        return self.nama

    class Meta:
        verbose_name = "Produk"
        verbose_name_plural = "Produk"
        ordering = ["-id"]


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    produk = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    jumlah = models.PositiveIntegerField(default=1)

    dibuat = models.DateTimeField(auto_now_add=True)
    diperbarui = models.DateTimeField(auto_now=True)

    @property
    def subtotal(self):
        return self.produk.harga_diskon * self.jumlah

    def __str__(self):
        return f"{self.user.username} - {self.produk.nama}"

    class Meta:
        verbose_name = "Keranjang"
        verbose_name_plural = "Keranjang"

        constraints = [
            models.UniqueConstraint(
                fields=["user", "produk"],
                name="unique_user_product_cart"
            )
        ]


class Order(models.Model):

    STATUS_CHOICES = [
        ("Menunggu Pembayaran", "Menunggu Pembayaran"),
        ("Menunggu Verifikasi", "Menunggu Verifikasi"),
        ("Diproses", "Diproses"),
        ("Dikirim", "Dikirim"),
        ("Selesai", "Selesai"),
        ("Dibatalkan", "Dibatalkan"),
    ]

    PAYMENT_CHOICES = [
        ("COD", "COD"),
        ("Transfer Bank", "Transfer Bank"),
        ("QRIS", "QRIS"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    nama = models.CharField(max_length=150)
    telepon = models.CharField(max_length=30)
    alamat = models.TextField()

    metode_pembayaran = models.CharField(
        max_length=50,
        choices=PAYMENT_CHOICES
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="Menunggu Pembayaran"
    )

    bukti_pembayaran = models.ImageField(
        upload_to="bukti_pembayaran/",
        blank=True,
        null=True
    )

    dibuat = models.DateTimeField(auto_now_add=True)
    diperbarui = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pesanan #{self.id} - {self.user.username}"

    class Meta:
        verbose_name = "Pesanan"
        verbose_name_plural = "Pesanan"
        ordering = ["-dibuat"]


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    produk = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_items"
    )

    jumlah = models.PositiveIntegerField(default=1)

    harga = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    @property
    def subtotal(self):
        return self.harga * self.jumlah

    def __str__(self):
        if self.produk:
            return f"{self.produk.nama} x {self.jumlah}"

        return f"Produk terhapus x {self.jumlah}"

    class Meta:
        verbose_name = "Item Pesanan"
        verbose_name_plural = "Item Pesanan"


class Wishlist(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="wishlists"
    )

    produk = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="wishlists"
    )

    dibuat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.produk.nama}"

    class Meta:
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlist"

        constraints = [
            models.UniqueConstraint(
                fields=["user", "produk"],
                name="unique_user_product_wishlist"
            )
        ]


class ContactMessage(models.Model):

    nama = models.CharField(max_length=150)
    email = models.EmailField()
    pesan = models.TextField()

    dibuat = models.DateTimeField(auto_now_add=True)

    sudah_dibaca = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nama} - {self.email}"

    class Meta:
        verbose_name = "Pesan Kontak"
        verbose_name_plural = "Pesan Kontak"
        ordering = ["-dibuat"]


class Subscriber(models.Model):

    email = models.EmailField(unique=True)

    dibuat = models.DateTimeField(auto_now_add=True)

    aktif = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Subscriber"
        verbose_name_plural = "Subscriber"
        ordering = ["-dibuat"]