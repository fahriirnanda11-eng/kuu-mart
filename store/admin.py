from django.contrib import admin
from .models import Category, Product, Cart, Order, OrderItem
from django.contrib import admin
from .models import Subscriber
from .models import ContactMessage


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

admin.site.register(Subscriber
                    )
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nama',
        'kategori',
        'harga',
        'stok',
        'diskon',
        'rating'
    )
    list_filter = ('kategori',)
    search_fields = ('nama',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'produk', 'jumlah', 'dibuat')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nama',
        'telepon',
        'metode_pembayaran',
        'total',
        'status',
        'dibuat'
    )

    list_filter = (
        'status',
        'dibuat'
    )

    search_fields = (
        'nama',
        'telepon'
    )

    list_editable = (
        'status',
    )

    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'produk',
        'jumlah',
        'harga'
    )

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        "nama",
        "email",
        "dibuat",
    )

    search_fields = (
        "nama",
        "email",
    )