from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name='index'),
    path('cart/', views.keranjang, name='cart'),
    path('cart/add/<int:product_id>/', 
         views . tambah_ke_keranjang,
         name='tambah_ke_keranjang'),
     path('beli/<int:product_id>/',
         views.beli_sekarang, name='beli_sekarang'),
         path('keranjang/tambah/<int:product_id>/',
     views.tambah_ke_keranjang,
     name='tambah_ke_keranjang'),
    path('cart/kurang/<int:id>/', views.kurang_keranjang,
          name='kurang_keranjang'),
    path('cart/hapus/<int:id>/', views.hapus_keranjang, 
         name='hapus_keranjang'),
    path('checkout/', views.checkout, 
         name='checkout'),
     path('order-succes/', views.order_succes,
          name='order_succes'),
     path('order/', views.riwayat_pesanan,
          name='riwayat_pesanan'),
     path('orders/<int:order_id>/',
          views.detail_order, name='detail_order'),
     path('payment/<int:order_id>/',
          views.payment,name='payment'),
     path('produk/', views.produk, name='produk'),
     path("subscribe/",views.subscribe,name="subscribe"),
     path('kategori/', views.kategori, name='kategori'),
     path('promo/', views.promo, name='promo'),
     path('tentang/', views.tentang, name='tentang'),
     path('kontak/', views.kontak, name='kontak'),
     path( 'produk/<int:product_id>/',views.detail_produk,name='detail_produk'),
     path('wishlist/<int:id>/',views.tambah_wishlist,name='wishlist'),
     path('wishlist/', views.wishlist, name='wishlist'),

]


