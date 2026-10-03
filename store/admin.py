from django.contrib import admin

from .models import (
    Category,
    Product,
    Cart,
    Order,
    OrderItem,
    Wishlist,
    ContactMessage,
    Subscriber,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "nama",
        "deskripsi",
    )

    search_fields = (
        "nama",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "nama",
        "kategori",
        "harga",
        "diskon",
        "stok",
        "rating",
        "terjual",
        "dibuat",
    )

    list_filter = (
        "kategori",
        "diskon",
        "dibuat",
    )

    search_fields = (
        "nama",
        "deskripsi",
    )

    ordering = (
        "-dibuat",
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "produk",
        "jumlah",
        "dibuat",
    )

    search_fields = (
        "user__username",
        "produk__nama",
    )


class OrderItemInline(admin.TabularInline):

    model = OrderItem

    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "nama",
        "telepon",
        "metode_pembayaran",
        "total",
        "status",
        "dibuat",
    )

    list_filter = (
        "status",
        "metode_pembayaran",
        "dibuat",
    )

    search_fields = (
        "nama",
        "telepon",
        "user__username",
    )

    ordering = (
        "-dibuat",
    )

    inlines = [
        OrderItemInline
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "produk",
        "jumlah",
        "harga",
        "subtotal",
    )


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "produk",
        "dibuat",
    )

    search_fields = (
        "user__username",
        "produk__nama",
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "nama",
        "email",
        "sudah_dibaca",
        "dibuat",
    )

    list_filter = (
        "sudah_dibaca",
        "dibuat",
    )

    search_fields = (
        "nama",
        "email",
        "pesan",
    )


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "email",
        "aktif",
        "dibuat",
    )

    list_filter = (
        "aktif",
    )

    search_fields = (
        "email",
    )