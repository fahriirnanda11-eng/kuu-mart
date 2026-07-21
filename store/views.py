from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, Order, OrderItem, Wishlist, ContactMessage
from django.shortcuts import render
from .models import Product, Category
from .models import Subscriber
from django.contrib import messages
from django.shortcuts import render, redirect

def kontak(request):
    if request.method == "POST":

        nama = request.POST.get("nama")
        email = request.POST.get("email")
        subjek = request.POST.get("subjek")
        pesan = request.POST.get("pesan")

        # Nanti bisa disimpan ke database atau dikirim email

        messages.success(request, "🎉 Pesan Anda berhasil terkirim! Kami akan segera menghubungi Anda.")

        return redirect("kontak")

    return render(request, "kontak.html")
def kurang_keranjang(request, id):
    item = get_object_or_404(Cart, id=id, user=request.user)

    if item.jumlah > 1:
        item.jumlah -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart')

@login_required
def tambah_ke_keranjang(request, product_id):
    produk = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(
        user=request.user,
        produk=produk
    )

    if not created:
        cart.jumlah += 1
        cart.save()

    return redirect('cart')

@login_required
def keranjang(request):
    carts = Cart.objects.filter(user=request.user)

    total = 0

    for item in carts:
        total += item.produk.harga_diskon * item.jumlah

    context = {
        "carts": carts,
        "total": total,
    }

    return render(request, "cart.html", context)

def hapus_keranjang(request, id):
    item = get_object_or_404(Cart, id=id, user=request.user)
    item.delete()
    return redirect('cart')


@login_required
def checkout(request):
    carts = Cart.objects.filter(user=request.user)

    total = 0

    for item in carts:
        total += item.produk.harga_diskon * item.jumlah

    if request.method == 'POST':

        order = Order.objects.create(
    user=request.user,
    nama=request.POST['nama'],
    telepon=request.POST['telepon'],
    alamat=request.POST['alamat'],
    metode_pembayaran=request.POST['metode'],
    total=total
    )
        
        for item in carts:
            OrderItem.objects.create(
        order=order,
        produk=item.produk,
        jumlah=item.jumlah,
        harga=item.produk.harga_diskon
    )

        carts.delete()
        if order.metode_pembayaran == "COD":
            order.status = "Diproses"
            order.save()
            return redirect("order_succes")
        return redirect("payment", order_id=order.id)

    return render(request, 'checkout.html', {
        'carts': carts,
        'total': total
    })

@login_required
def beli_sekarang(request, product_id):
    produk = get_object_or_404(Product, id=product_id)

    # Kosongkan keranjang lama
    Cart.objects.filter(user=request.user).delete()

    # Tambahkan produk yang dipilih
    Cart.objects.create(
        user=request.user,
        produk=produk,
        jumlah=1
    )

    return redirect('checkout')

@login_required
def order_succes(request):
    return render(request, 'order_succes.html')

@login_required
def riwayat_pesanan(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-dibuat')

    return render(request,
                  'orders.html',
                  {'orders': orders})

@login_required
def detail_order(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)

    items = OrderItem.objects.filter(order=order)

    return render(request, 'detail_order.html', {
        'order': order,
        'items': items
    })

def index(request):
    produk = Product.objects.all().order_by('-id')
    kategori = Category.objects.all()

    jumlah_pesanan = 0

    if request.user.is_authenticated:
        jumlah_pesanan = Order.objects.filter(
            user=request.user
        ).exclude(status='Selesai').count()

    context = {
        'produk': produk,
        'kategori': kategori,
        'jumlah_pesanan': jumlah_pesanan,
    }

    return render(request, 'index.html', context)

@login_required
def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == "POST":
        if request.FILES.get("bukti"):
            order.bukti_pembayaran = request.FILES["bukti"]
            order.status = "Menunggu Verifikasi"
            order.save()
            return redirect("detail_order", order_id=order.id)

    return render(request, "payment.html", {
        "order": order
    })
    

def produk(request):

    produk = Product.objects.all().order_by('-id')
    kategori = Category.objects.all()

    q = request.GET.get("q")
    kategori_id = request.GET.get("kategori")

    if q:
        produk = produk.filter(nama__icontains=q)

    if kategori_id:
        produk = produk.filter(kategori_id=kategori_id)

    context = {
        "produk": produk,
        "kategori": kategori,
    }

    return render(request, "produk.html", context)

def subscribe(request):

    if request.method == "POST":

        email = request.POST.get("email")

        if email:
            Subscriber.objects.get_or_create(email=email)

            messages.success(
                request,
                "Terima kasih telah berlangganan!"
            )

    return redirect("index")

def kategori(request):
    kategori = Category.objects.all()

    return render(request, 'kategori.html', {
        'kategori': kategori
    })


def promo(request):

    produk = Product.objects.filter(diskon__gt=0).order_by('-diskon')

    return render(request, 'promo.html', {
        'produk': produk
    })


def tentang(request):
    return render(request, 'tentang.html')


def kontak(request):

    if request.method == "POST":

        ContactMessage.objects.create(
            nama=request.POST.get("nama"),
            email=request.POST.get("email"),
            pesan=request.POST.get("pesan"),
        )

        messages.success(
            request,
            "🎉 Pesan Anda berhasil terkirim! Kami akan segera menghubungi Anda."
        )

        return redirect("kontak")

    return render(request, "kontak.html")

def detail_produk(request, product_id):

    produk = get_object_or_404(Product, id=product_id)

    produk_lain = Product.objects.exclude(
        id=product_id
    ).order_by('?')[:4]

    return render(request, 'detail_produk.html', {
        'produk': produk,
        'produk_lain': produk_lain,
    })

@login_required
def tambah_wishlist(request, id):
    produk = get_object_or_404(Product, id=id)

    Wishlist.objects.get_or_create(
        user=request.user,
        produk=produk
    )

    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)

    return render(request, 'wishlist.html', {
        'wishlist': wishlist
    })