from django.urls import path
from . import views


urlpatterns = [

    # =====================================================
    # BERANDA
    # =====================================================

    path(
        "",
        views.index,
        name="index"
    ),


    # =====================================================
    # PRODUK
    # =====================================================

    path(
        "produk/",
        views.produk,
        name="produk"
    ),

    path(
        "produk/<int:product_id>/",
        views.detail_produk,
        name="detail_produk"
    ),


    # =====================================================
    # KATEGORI & PROMO
    # =====================================================

    path(
        "kategori/",
        views.kategori,
        name="kategori"
    ),

    path(
        "promo/",
        views.promo,
        name="promo"
    ),


    # =====================================================
    # TENTANG & KONTAK
    # =====================================================

    path(
        "tentang/",
        views.tentang,
        name="tentang"
    ),

    path(
        "kontak/",
        views.kontak,
        name="kontak"
    ),


    # =====================================================
    # SUBSCRIBE
    # =====================================================

    path(
        "subscribe/",
        views.subscribe,
        name="subscribe"
    ),


    # =====================================================
    # SERVICE WORKER
    # =====================================================

    path(
        "service-worker.js",
        views.service_worker,
        name="service_worker"
    ),


    # =====================================================
    # KERANJANG
    # =====================================================

    path(
        "cart/",
        views.keranjang,
        name="cart"
    ),

    path(
        "keranjang/",
        views.keranjang,
        name="keranjang"
    ),

    path(
        "cart/tambah/<int:product_id>/",
        views.tambah_ke_keranjang,
        name="tambah_ke_keranjang"
    ),

    path(
        "cart/kurang/<int:id>/",
        views.kurang_keranjang,
        name="kurang_keranjang"
    ),

    path(
        "cart/hapus/<int:id>/",
        views.hapus_keranjang,
        name="hapus_keranjang"
    ),


    # =====================================================
    # BELI SEKARANG & CHECKOUT
    # =====================================================

    path(
        "beli/<int:product_id>/",
        views.beli_sekarang,
        name="beli_sekarang"
    ),

    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),


    # =====================================================
    # PESANAN
    # =====================================================

    path(
        "pesanan/sukses/",
        views.order_succes,
        name="order_succes"
    ),

    path(
        "pesanan/",
        views.riwayat_pesanan,
        name="riwayat_pesanan"
    ),

    path(
        "pesanan/<int:order_id>/",
        views.detail_order,
        name="detail_order"
    ),


    # =====================================================
    # PEMBAYARAN
    # =====================================================

    path(
        "payment/<int:order_id>/",
        views.payment,
        name="payment"
    ),


    # =====================================================
    # WISHLIST
    # =====================================================

    path(
        "wishlist/",
        views.wishlist,
        name="wishlist"
    ),

    path(
        "wishlist/tambah/<int:product_id>/",
        views.tambah_wishlist,
        name="tambah_wishlist"
    ),

    path(
        "wishlist/hapus/<int:product_id>/",
        views.hapus_wishlist,
        name="hapus_wishlist"
    ),
]