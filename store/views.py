from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from .models import (
    Product,
    Category,
    Cart,
    Order,
    OrderItem,
    Wishlist,
    ContactMessage,
    Subscriber,
)


# =========================================================
# SERVICE WORKER
# =========================================================

def service_worker(request):
    return HttpResponse(
        """
        self.addEventListener('install', event => {
            self.skipWaiting();
        });

        self.addEventListener('activate', event => {
            event.waitUntil(clients.claim());
        });

        self.addEventListener('fetch', event => {
        });
        """,
        content_type="application/javascript"
    )


# =========================================================
# BERANDA
# =========================================================

def index(request):

    produk = Product.objects.all().order_by("-id")

    kategori = Category.objects.all()

    # PRODUK PROMO
    produk_promo = Product.objects.filter(
        diskon__gt=0
    ).order_by("-diskon", "-id")

    jumlah_pesanan = 0
    jumlah_keranjang = 0
    jumlah_wishlist = 0

    if request.user.is_authenticated:

        jumlah_pesanan = Order.objects.filter(
            user=request.user
        ).exclude(
            status="Selesai"
        ).count()

        jumlah_keranjang = Cart.objects.filter(
            user=request.user
        ).count()

        jumlah_wishlist = Wishlist.objects.filter(
            user=request.user
        ).count()

    return render(
        request,
        "index.html",
        {
            "produk": produk,
            "produk_promo": produk_promo,
            "kategori": kategori,
            "jumlah_pesanan": jumlah_pesanan,
            "jumlah_keranjang": jumlah_keranjang,
            "jumlah_wishlist": jumlah_wishlist,
        }
    )


# =========================================================
# PRODUK
# =========================================================

def produk(request):

    produk_list = Product.objects.all().order_by("-id")

    kategori = Category.objects.all()

    q = request.GET.get("q")
    kategori_id = request.GET.get("kategori")

    if q:
        produk_list = produk_list.filter(
            nama__icontains=q
        )

    if kategori_id:
        produk_list = produk_list.filter(
            kategori_id=kategori_id
        )

    return render(
        request,
        "produk.html",
        {
            "produk": produk_list,
            "kategori": kategori,
        }
    )


# =========================================================
# DETAIL PRODUK
# =========================================================

def detail_produk(request, product_id):

    produk = get_object_or_404(
        Product,
        id=product_id
    )

    produk_lain = Product.objects.exclude(
        id=product_id
    ).order_by("?")[:4]

    return render(
        request,
        "detail_produk.html",
        {
            "produk": produk,
            "produk_lain": produk_lain,
        }
    )


# =========================================================
# KATEGORI
# =========================================================

def kategori(request):

    kategori_list = Category.objects.all()

    return render(
        request,
        "kategori.html",
        {
            "kategori": kategori_list
        }
    )


# =========================================================
# PROMO
# =========================================================

def promo(request):

    produk = Product.objects.filter(
        diskon__gt=0
    ).order_by(
        "-diskon",
        "-id"
    )

    return render(
        request,
        "promo.html",
        {
            "produk": produk
        }
    )


# =========================================================
# TENTANG
# =========================================================

def tentang(request):

    return render(
        request,
        "tentang.html"
    )


# =========================================================
# KONTAK
# =========================================================

def kontak(request):

    if request.method == "POST":

        ContactMessage.objects.create(
            nama=request.POST.get("nama", ""),
            email=request.POST.get("email", ""),
            pesan=request.POST.get("pesan", "")
        )

        messages.success(
            request,
            "Pesan berhasil dikirim."
        )

        return redirect("kontak")

    return render(
        request,
        "kontak.html"
    )


# =========================================================
# SUBSCRIBE
# =========================================================

def subscribe(request):

    if request.method == "POST":

        email = request.POST.get("email")

        if email:

            Subscriber.objects.get_or_create(
                email=email
            )

            messages.success(
                request,
                "Terima kasih telah berlangganan!"
            )

    return redirect("index")


# =========================================================
# KERANJANG
# =========================================================

@login_required
def keranjang(request):

    carts = Cart.objects.filter(
        user=request.user
    ).select_related(
        "produk"
    )

    total = sum(
        item.subtotal
        for item in carts
    )

    return render(
        request,
        "cart.html",
        {
            "carts": carts,
            "total": total,
        }
    )


# =========================================================
# TAMBAH KE KERANJANG
# =========================================================

@login_required
def tambah_ke_keranjang(request, product_id):

    produk = get_object_or_404(
        Product,
        id=product_id
    )

    # CEK STOK
    if produk.stok <= 0:

        messages.error(
            request,
            "Maaf, stok produk sedang habis."
        )

        return redirect("produk")

    cart, created = Cart.objects.get_or_create(
        user=request.user,
        produk=produk
    )

    if not created:

        # Jangan melebihi stok
        if cart.jumlah >= produk.stok:

            messages.warning(
                request,
                "Jumlah produk di keranjang sudah mencapai stok yang tersedia."
            )

            return redirect("cart")

        cart.jumlah += 1
        cart.save()

    messages.success(
        request,
        f"{produk.nama} berhasil ditambahkan ke keranjang."
    )

    return redirect("cart")


# =========================================================
# KURANGI KERANJANG
# =========================================================

@login_required
def kurang_keranjang(request, id):

    item = get_object_or_404(
        Cart,
        id=id,
        user=request.user
    )

    if item.jumlah > 1:

        item.jumlah -= 1
        item.save()

    else:

        item.delete()

    return redirect("cart")


# =========================================================
# HAPUS KERANJANG
# =========================================================

@login_required
def hapus_keranjang(request, id):

    item = get_object_or_404(
        Cart,
        id=id,
        user=request.user
    )

    item.delete()

    messages.success(
        request,
        "Produk berhasil dihapus dari keranjang."
    )

    return redirect("cart")


# =========================================================
# BELI SEKARANG
# =========================================================

@login_required
def beli_sekarang(request, product_id):

    produk = get_object_or_404(
        Product,
        id=product_id
    )

    # Bersihkan keranjang sementara
    # lalu masukkan produk yang ingin dibeli
    Cart.objects.filter(
        user=request.user
    ).delete()

    Cart.objects.create(
        user=request.user,
        produk=produk,
        jumlah=1
    )

    return redirect("checkout")


# =========================================================
# CHECKOUT
# =========================================================

@login_required
def checkout(request):

    carts = Cart.objects.filter(
        user=request.user
    ).select_related(
        "produk"
    )

    if not carts.exists():

        messages.warning(
            request,
            "Keranjang Anda masih kosong."
        )

        return redirect("cart")

    total = sum(
        item.subtotal
        for item in carts
    )

    if request.method == "POST":

        nama = request.POST.get(
            "nama",
            ""
        )

        telepon = request.POST.get(
            "telepon",
            ""
        )

        alamat = request.POST.get(
            "alamat",
            ""
        )

        metode = request.POST.get(
            "metode",
            "COD"
        )

        order = Order.objects.create(
            user=request.user,
            nama=nama,
            telepon=telepon,
            alamat=alamat,
            metode_pembayaran=metode,
            total=total
        )

        for item in carts:

            OrderItem.objects.create(
                order=order,
                produk=item.produk,
                jumlah=item.jumlah,
                harga=item.produk.harga_diskon
            )

            item.produk.terjual += item.jumlah

            if item.produk.stok >= item.jumlah:

                item.produk.stok -= item.jumlah

            else:

                item.produk.stok = 0

            item.produk.save()

        carts.delete()

        # COD langsung diproses
        if metode == "COD":

            order.status = "Diproses"
            order.save()

            return redirect(
                "order_succes"
            )

        # Transfer / QRIS menuju pembayaran
        return redirect(
            "payment",
            order_id=order.id
        )

    return render(
        request,
        "checkout.html",
        {
            "carts": carts,
            "total": total,
        }
    )


# =========================================================
# PESANAN SUKSES
# =========================================================

@login_required
def order_succes(request):

    return render(
        request,
        "order_succes.html"
    )


# =========================================================
# RIWAYAT PESANAN
# =========================================================

@login_required
def riwayat_pesanan(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by(
        "-dibuat"
    )

    return render(
        request,
        "orders.html",
        {
            "orders": orders
        }
    )


# =========================================================
# DETAIL PESANAN
# =========================================================

@login_required
def detail_order(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    items = order.items.select_related(
        "produk"
    )

    return render(
        request,
        "detail_order.html",
        {
            "order": order,
            "items": items
        }
    )


# =========================================================
# PEMBAYARAN
# =========================================================

@login_required
def payment(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    if request.method == "POST":

        bukti = request.FILES.get(
            "bukti_pembayaran"
        )

        if not bukti:

            bukti = request.FILES.get(
                "bukti"
            )

        if bukti:

            order.bukti_pembayaran = bukti

            order.status = "Menunggu Verifikasi"

            order.save()

            messages.success(
                request,
                "Bukti pembayaran berhasil dikirim."
            )

            return redirect(
                "detail_order",
                order_id=order.id
            )

        messages.error(
            request,
            "Silakan pilih bukti pembayaran."
        )

    return render(
        request,
        "payment.html",
        {
            "order": order
        }
    )


# =========================================================
# WISHLIST
# =========================================================

@login_required
def wishlist(request):

    wishlist_items = Wishlist.objects.filter(
        user=request.user
    ).select_related(
        "produk",
        "produk__kategori"
    )

    return render(
        request,
        "wishlist.html",
        {
            "wishlist": wishlist_items
        }
    )


# =========================================================
# TAMBAH WISHLIST
# =========================================================

@login_required
def tambah_wishlist(request, product_id):

    produk = get_object_or_404(
        Product,
        id=product_id
    )

    wishlist, created = Wishlist.objects.get_or_create(
        user=request.user,
        produk=produk
    )

    if created:

        messages.success(
            request,
            f"{produk.nama} ditambahkan ke wishlist."
        )

    else:

        messages.info(
            request,
            "Produk sudah ada di wishlist."
        )

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "index"
        )
    )


# =========================================================
# HAPUS WISHLIST
# =========================================================

@login_required
def hapus_wishlist(request, product_id):

    Wishlist.objects.filter(
        user=request.user,
        produk_id=product_id
    ).delete()

    messages.success(
        request,
        "Produk dihapus dari wishlist."
    )

    return redirect(
        "wishlist"
    )